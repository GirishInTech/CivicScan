from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import UserProfile
from reports.models import Report

class Command(BaseCommand):
    help = 'Delete all users except admin and aman, along with their associated data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        # Users to keep
        keep_users = ['admin', 'aman']
        
        # Get users to delete
        users_to_delete = User.objects.exclude(username__in=keep_users)
        
        if options['dry_run']:
            self.stdout.write("DRY RUN - Would delete the following:")
            self.stdout.write(f"Users to delete: {users_to_delete.count()}")
            for user in users_to_delete:
                report_count = Report.objects.filter(user=user).count()
                self.stdout.write(f"  - {user.username} (Reports: {report_count})")
            return

        # Confirm deletion
        self.stdout.write(f"About to delete {users_to_delete.count()} users:")
        for user in users_to_delete:
            report_count = Report.objects.filter(user=user).count()
            self.stdout.write(f"  - {user.username} (Reports: {report_count})")
        
        self.stdout.write("\nThis will delete:")
        self.stdout.write("1. User accounts")
        self.stdout.write("2. UserProfile objects")
        self.stdout.write("3. All reports by these users")
        
        # Ask for confirmation
        confirm = input("\nAre you sure you want to proceed? (yes/no): ")
        if confirm.lower() != 'yes':
            self.stdout.write("Deletion cancelled.")
            return

        deleted_users = 0
        deleted_reports = 0
        deleted_profiles = 0

        for user in users_to_delete:
            # Delete reports by this user
            user_reports = Report.objects.filter(user=user)
            report_count = user_reports.count()
            user_reports.delete()
            deleted_reports += report_count
            
            # Delete user profile
            try:
                profile = UserProfile.objects.get(user=user)
                profile.delete()
                deleted_profiles += 1
            except UserProfile.DoesNotExist:
                pass
            
            # Delete user
            username = user.username
            user.delete()
            deleted_users += 1
            
            self.stdout.write(f"Deleted user: {username} (Reports: {report_count})")

        self.stdout.write(
            self.style.SUCCESS(
                f'\nDeletion completed successfully!\n'
                f'Deleted users: {deleted_users}\n'
                f'Deleted profiles: {deleted_profiles}\n'
                f'Deleted reports: {deleted_reports}'
            )
        )
        
        # Show remaining users
        remaining_users = User.objects.all()
        self.stdout.write(f"\nRemaining users ({remaining_users.count()}):")
        for user in remaining_users:
            report_count = Report.objects.filter(user=user).count()
            self.stdout.write(f"  - {user.username} (Reports: {report_count})") 