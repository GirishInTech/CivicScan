from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.management import CommandError
import getpass

class Command(BaseCommand):
    help = 'Change all user passwords except admin'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            type=str,
            help='The new password to set for all users (will prompt if not provided)'
        )

    def handle(self, *args, **options):
        # Get all users except admin
        users = User.objects.exclude(username='admin')
        
        # Get password from argument or prompt
        password = options.get('password')
        if not password:
            password = getpass.getpass('Enter new password for all users: ')
            
        if not password:
            raise CommandError('Password cannot be empty')
            
        updated_count = 0
        
        self.stdout.write(f"Changing passwords for {users.count()} users...")
        
        for user in users:
            user.set_password(password)
            user.save()
            updated_count += 1
            self.stdout.write(f"✓ Password changed for: {user.username}")
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully changed passwords for {updated_count} users'
            )
        )
        
        self.stdout.write("Users updated:")
        for user in users:
            self.stdout.write(f"  - {user.username} ({user.first_name} {user.last_name})")