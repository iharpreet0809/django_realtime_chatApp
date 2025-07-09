import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from chat_app.models import ChatRoom, Message, Profile

class Command(BaseCommand):
    help = 'Seeds the database with sample users, chat rooms, and messages.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # --- Clean up existing data ---
        User.objects.filter(is_superuser=False).delete()
        ChatRoom.objects.all().delete()
        Message.objects.all().delete()

        # --- Create Sample Users ---
        users_data = [
            {'username': 'alice', 'email': 'alice@example.com', 'phone': '1112223331'},
            {'username': 'bob', 'email': 'bob@example.com', 'phone': '1112223332'},
            {'username': 'charlie', 'email': 'charlie@example.com', 'phone': '1112223333'},
        ]
        users = []
        for data in users_data:
            user = User.objects.create_user(username=data['username'], email=data['email'], password='password123')
            user.profile.phone_number = data['phone']
            user.profile.save()
            users.append(user)
            self.stdout.write(f'Created user: {user.username}')

        # --- Create One-on-One Chats ---
        alice, bob, charlie = users[0], users[1], users[2]

        # Alice and Bob
        room1 = ChatRoom.objects.create(name=f"{alice.username}_{bob.username}", is_group_chat=False)
        room1.participants.add(alice, bob)
        self.stdout.write(f'Created chat between {alice.username} and {bob.username}')

        # Alice and Charlie
        room2 = ChatRoom.objects.create(name=f"{alice.username}_{charlie.username}", is_group_chat=False)
        room2.participants.add(alice, charlie)
        self.stdout.write(f'Created chat between {alice.username} and {charlie.username}')
        
        # --- Create Sample Messages ---
        messages = [
            (room1, alice, "Hey Bob, how's it going?"),
            (room1, bob, "Hey Alice! Going well, just working on the new project. You?"),
            (room1, alice, "Same here. It's a lot of work but exciting!"),
            (room2, alice, "Hi Charlie, do you have the report?"),
            (room2, charlie, "Yep, sending it over now."),
        ]
        
        for room, sender, content in messages:
            Message.objects.create(room=room, sender=sender, content=content)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(users)} users and {len(messages)} messages.'))