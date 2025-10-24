from rest_framework import generics, status, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile, ChatRoom, Message
from .serializers import UserSerializer, ProfileSerializer, ChatRoomSerializer, MessageSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

# ... (SignUpView, LoginView, ProfileView remain the same) ...
class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []


#login view
class LoginView(APIView):
    permission_classes = []
    def post(self, request):
        from django.contrib.auth import login
        
        # Support both old 'username' and new 'identifier' fields for backward compatibility
        identifier = request.data.get('identifier') or request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(request, identifier=identifier, password=password)
        if user:
            # Create API token
            token, _ = Token.objects.get_or_create(user=user)
            
            # Also log user into Django session for template access
            login(request, user)
            
            return Response({
                'token': token.key, 
                'username': user.username,
                'first_name': user.first_name or user.username
            })
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_object(self):
        return self.request.user.profile


class StartChatView(APIView):
    """
    Starts a new one-on-one chat with a user by their email or phone number.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        identifier = request.data.get('identifier') # Can be email or phone
        if not identifier:
            return Response({'error': 'Email or phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Find the target user by email or phone number
            target_user = User.objects.get(Q(email=identifier) | Q(profile__phone_number=identifier))
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if target_user == request.user:
            return Response({'error': 'You cannot start a chat with yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a one-on-one chat room already exists
        user1 = request.user
        user2 = target_user
        
        existing_room = ChatRoom.objects.filter(
            is_group_chat=False, participants=user1
        ).filter(
            participants=user2
        ).first()

        if existing_room:
            serializer = ChatRoomSerializer(existing_room)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If not, create a new chat room
        room_name = f"{user1.username}_{user2.username}"
        new_room = ChatRoom.objects.create(name=room_name, is_group_chat=False)
        new_room.participants.add(user1, user2)
        
        # Notify both users about the new chat room via WebSocket
        channel_layer = get_channel_layer()
        room_data = ChatRoomSerializer(new_room).data
        
        # Send to presence group for all users to receive
        async_to_sync(channel_layer.group_send)(
            "presence",
            {
                "type": "new_chat_created",
                "room_data": room_data,
                "participants": [user1.id, user2.id]
            }
        )
        
        serializer = ChatRoomSerializer(new_room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChatRoomListView(generics.ListCreateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.chat_rooms.all()

    # We use StartChatView for creating one-on-one chats now.
    # This can be used for creating group chats.
    def perform_create(self, serializer):
        participant_ids = self.request.data.get('participants', [])
        participants = User.objects.filter(id__in=participant_ids)
        room = serializer.save(is_group_chat=True) # Assuming this endpoint is for groups now
        room.participants.add(self.request.user, *participants)


class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        room = get_object_or_404(ChatRoom, id=room_id, participants=self.request.user)
        return Message.objects.filter(room=room)

    def perform_create(self, serializer):
        room_id = self.kwargs['room_id']
        room = get_object_or_404(ChatRoom, id=room_id, participants=self.request.user)
        serializer.save(sender=self.request.user, room=room)


class MarkMessagesSeenView(APIView):
    """Mark all messages in a room as seen by the current user"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, room_id):
        from .models import MessageStatus
        room = get_object_or_404(ChatRoom, id=room_id, participants=request.user)
        
        # Update all message statuses for this user in this room to 'seen'
        updated_count = MessageStatus.objects.filter(
            message__room=room,
            user=request.user,
            status__in=['sent', 'delivered']
        ).update(status='seen')
        
        return Response({
            'success': True, 
            'updated_count': updated_count
        })