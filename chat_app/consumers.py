import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.utils import timezone
from .models import Message, ChatRoom, Profile, MessageStatus

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        self.room = await self.get_room()
        if self.room is None:
            await self.close(code=4001)
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'chat_message':
            message = await self.save_message(data)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'broadcast_message',
                    'message': {
                        'id': message.id,
                        'sender': message.sender.username,
                        'content': message.content,
                        'image': message.image.url if message.image else None,
                        'timestamp': message.timestamp.isoformat(),
                    }
                }
            )
        elif message_type == 'message_seen':
            # This is triggered when a user opens a chat and sees messages
            updated_status = await self.mark_message_as_seen(data['message_id'])
            if updated_status:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'broadcast_seen_status',
                        'message_id': data['message_id'],
                        'seen_by_user': self.user.username,
                        'status': 'seen'
                    }
                )

    # --- Broadcast Handlers ---
    async def broadcast_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    async def broadcast_seen_status(self, event):
        await self.send(text_data=json.dumps({
            'type': 'seen_update',
            'message_id': event['message_id'],
            'seen_by_user': event['seen_by_user'],
            'status': event['status']
        }))

    # --- Database Methods ---
    @database_sync_to_async
    def get_room(self):
        try:
            return ChatRoom.objects.get(id=self.room_id, participants=self.user)
        except ChatRoom.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, data):
        content = data.get('message')
        image_data = data.get('image')
        
        message = Message.objects.create(room=self.room, sender=self.user, content=content)
        
        if image_data:
            try:
                format, imgstr = image_data.split(';base64,') 
                ext = format.split('/')[-1] 
                file_data = ContentFile(base64.b64decode(imgstr), name=f'{message.id}.{ext}')
                message.image = file_data
                message.save()
            except Exception as e:
                print(f"Error saving image: {e}")

        for participant in self.room.participants.all():
            status = 'seen' if participant == self.user else 'delivered'
            MessageStatus.objects.create(message=message, user=participant, status=status)
        return message

    @database_sync_to_async
    def mark_message_as_seen(self, message_id):
        try:
            message_status = MessageStatus.objects.get(message__id=message_id, user=self.user)
            if message_status.status != 'seen':
                message_status.status = 'seen'
                message_status.timestamp = timezone.now()
                message_status.save()
                return message_status
        except MessageStatus.DoesNotExist:
            pass
        return None

# PresenceConsumer remains the same as it's already robust
class PresenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return
        
        self.group_name = "presence"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.update_status('Available')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.update_status('Offline')

    async def receive(self, text_data):
        data = json.loads(text_data)
        status = data.get('status')
        if status in [s[0] for s in Profile.STATUS_CHOICES]:
            await self.update_status(status)

    async def user_status_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'presence',
            'payload': event['payload']
        }))

    @database_sync_to_async
    def update_status(self, status):
        profile = self.user.profile
        profile.status = status
        profile.last_seen = timezone.now()
        profile.save()
        
        payload = {
            "user_id": self.user.id,
            "username": self.user.username,
            "status": status,
            "last_seen": profile.last_seen.isoformat()
        }

        self.channel_layer.group_send(
            self.group_name,
            {
                "type": "user.status.update",
                "payload": payload
            }
        )