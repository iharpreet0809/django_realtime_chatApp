from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Test database connection and basic operations'

    def handle(self, *args, **options):
        try:
            # Test database connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                self.stdout.write(
                    self.style.SUCCESS(f'Database connection successful: {result}')
                )
            
            # Test model operations
            user_count = User.objects.count()
            self.stdout.write(
                self.style.SUCCESS(f'User count: {user_count}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Database error: {str(e)}')
            )