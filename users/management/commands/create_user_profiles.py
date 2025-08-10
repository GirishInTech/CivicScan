from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import UserProfile

class Command(BaseCommand):
    help = 'Create UserProfile objects for users that don\'t have them'

    def handle(self, *args, **options):
        created_count = 0
        existing_count = 0

        for user in User.objects.all():
            try:
                # Try to get existing profile
                profile = UserProfile.objects.get(user=user)
                existing_count += 1
                self.stdout.write(f"Profile already exists for user: {user.username}")
            except UserProfile.DoesNotExist:
                # Create new profile
                profile = UserProfile.objects.create(
                    user=user,
                    phone_number="N/A"  # Default phone number
                )
                created_count += 1
                self.stdout.write(f"Created profile for user: {user.username}")

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} new profiles. {existing_count} profiles already existed.'
            )
        ) 