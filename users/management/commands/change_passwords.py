from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Change all user passwords except admin to 1234'

    def handle(self, *args, **options):
        # Get all users except admin
        users = User.objects.exclude(username='admin')
        
        password = '1234'
        updated_count = 0
        
        self.stdout.write(f"Changing passwords for {users.count()} users...")
        
        for user in users:
            user.set_password(password)
            user.save()
            updated_count += 1
            self.stdout.write(f"✓ Password changed for: {user.username}")
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully changed passwords for {updated_count} users to "{password}"'
            )
        )
        
        self.stdout.write("Users updated:")
        for user in users:
            self.stdout.write(f"  - {user.username} ({user.first_name} {user.last_name})")