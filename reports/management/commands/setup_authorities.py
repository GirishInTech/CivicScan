from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from reports.models import Report

class Command(BaseCommand):
    help = 'Sets up authority users and permissions for report management'

    def handle(self, *args, **kwargs):
        # Create Authority group if it doesn't exist
        authority_group, created = Group.objects.get_or_create(name='Authorities')
        
        if created:
            self.stdout.write(self.style.SUCCESS("Created 'Authorities' group"))
        
        # Get Report content type
        report_content_type = ContentType.objects.get_for_model(Report)
        
        # Add permissions to the Authority group
        permissions = [
            'view_report',
            'change_report', 
            'delete_report',
        ]
        
        for perm_codename in permissions:
            try:
                permission = Permission.objects.get(
                    codename=perm_codename,
                    content_type=report_content_type
                )
                authority_group.permissions.add(permission)
                self.stdout.write(f"Added {perm_codename} permission to Authorities group")
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Permission {perm_codename} not found"))
        
        # Create a sample authority user
        authority_user, created = User.objects.get_or_create(
            username='authority1',
            defaults={
                'first_name': 'City',
                'last_name': 'Authority',
                'email': 'authority@civicscan.com',
                'is_staff': True,  # Can access admin
            }
        )
        
        if created:
            authority_user.set_password('authority123')  # Set a default password
            authority_user.save()
            self.stdout.write(self.style.SUCCESS("Created authority user: authority1 (password: authority123)"))
        
        # Add user to Authority group
        authority_user.groups.add(authority_group)
        self.stdout.write(self.style.SUCCESS(f"Added {authority_user.username} to Authorities group"))
        
        self.stdout.write(self.style.SUCCESS("Authority setup completed!"))