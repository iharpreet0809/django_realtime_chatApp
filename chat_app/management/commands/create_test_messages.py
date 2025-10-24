from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from chat_app.models import ChatRoom, Message, MessageStatus
from django.utils import timezone
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Create test messages with different dates for testing date separators'

    def handle(self, *args, **options):
        try:
            admin = User.objects.get(username='admin')
            harry = User.objects.get(username='harry')
            room = ChatRoom.objects.filter(participants=admin).filter(participants=harry).first()
            
            if not room:
                self.stdout.write(self.style.ERROR('No chat room found between admin and harry'))
                return
            
            # Clear existing messages
            Message.objects.filter(room=room).delete()
            
            now = timezone.now()
            
            # Create messages for different dates
            test_messages = [
                # Today
                (now - timedelta(hours=2), admin, "Good morning Harry!"),
                (now - timedelta(hours=1), harry, "Good morning Admin!"),
                (now - timedelta(minutes=30), admin, "How are you today?"),
                (now - timedelta(minutes=15), harry, "I'm doing great, thanks!"),
                
                # Yesterday
                (now - timedelta(days=1, hours=10), admin, "Did you finish the project?"),
                (now - timedelta(days=1, hours=9), harry, "Yes, I completed it yesterday"),
                (now - timedelta(days=1, hours=8), admin, "Excellent work!"),
                
                # Day before yesterday (will show as weekday)
                (now - timedelta(days=2, hours=14), harry, "Let's meet tomorrow"),
                (now - timedelta(days=2, hours=13), admin, "Sure, what time?"),
                (now - timedelta(days=2, hours=12), harry, "How about 2 PM?"),
                
                # A week ago (will show date)
                (now - timedelta(days=7, hours=16), admin, "Happy to work with you"),
                (now - timedelta(days=7, hours=15), harry, "Same here!"),
                
                # Two weeks ago (will show date)
                (now - timedelta(days=14, hours=10), admin, "Welcome to the team"),
                (now - timedelta(days=14, hours=9), harry, "Thank you for the warm welcome"),
            ]
            
            created_count = 0
            for timestamp, sender, content in test_messages:
                message = Message.objects.create(
                    room=room,
                    sender=sender,
                    content=content,
                    timestamp=timestamp
                )
                
                # Create message status for both participants
                for participant in room.participants.all():
                    status = 'seen' if participant == sender else 'delivered'
                    MessageStatus.objects.create(
                        message=message,
                        user=participant,
                        status=status
                    )
                
                created_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {created_count} test messages with different dates')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating test messages: {str(e)}')
            )