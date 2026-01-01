from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from .models import Report

@receiver(post_save, sender=Report)
def report_status_changed(sender, instance, created, **kwargs):
    """
    Signal handler that triggers when a report is saved.
    Sends real-time notifications to users when their report status changes.
    """
    if not created:  # Only send notifications for updates, not new reports
        # Get the channel layer
        channel_layer = get_channel_layer()
        
        if channel_layer and instance.user:
            # Create the user group name
            user_group_name = f"user_{instance.user.id}"
            
            # Determine the status message
            status_messages = {
                'pending': 'Your report is pending review',
                'under_review': f'Your report is now being reviewed by {instance.reviewed_by.first_name if instance.reviewed_by else "an authority"}',
                'resolved': f'Your report has been resolved by {instance.reviewed_by.first_name if instance.reviewed_by else "an authority"}',
                'rejected': f'Your report has been rejected by {instance.reviewed_by.first_name if instance.reviewed_by else "an authority"}',
            }
            
            # Prepare notification data
            notification_data = {
                'report_id': instance.id,
                'status': instance.workflow_status,
                'message': status_messages.get(instance.workflow_status, 'Your report status has been updated'),
                'authority': f"{instance.reviewed_by.first_name} {instance.reviewed_by.last_name}".strip() if instance.reviewed_by else None,
                'authority_username': instance.reviewed_by.username if instance.reviewed_by else None,
                'timestamp': instance.reviewed_at.isoformat() if instance.reviewed_at else instance.submitted_at.isoformat(),
                'authority_comments': instance.authority_comments,
            }
            
            # Send to the user's WebSocket group
            try:
                async_to_sync(channel_layer.group_send)(
                    user_group_name,
                    {
                        'type': 'report_status_update',
                        'data': notification_data
                    }
                )
            except Exception as e:
                # Log error but don't fail the save operation
                print(f"Error sending WebSocket notification: {e}")

def send_custom_notification(user_id, notification_type, title, message, extra_data=None):
    """
    Utility function to send custom notifications to a specific user.
    
    Args:
        user_id: The ID of the user to notify
        notification_type: Type of notification (success, info, warning, error)
        title: Notification title
        message: Notification message
        extra_data: Additional data to include
    """
    channel_layer = get_channel_layer()
    
    if channel_layer:
        user_group_name = f"user_{user_id}"
        
        notification_data = {
            'type': notification_type,
            'title': title,
            'message': message,
            'timestamp': json.dumps({}),  # Current timestamp will be added by frontend
        }
        
        if extra_data:
            notification_data.update(extra_data)
        
        try:
            async_to_sync(channel_layer.group_send)(
                user_group_name,
                {
                    'type': 'notification',
                    'data': notification_data
                }
            )
        except Exception as e:
            print(f"Error sending custom notification: {e}")

def notify_all_authorities(title, message, notification_type='info'):
    """
    Send notifications to all users in the 'Authorities' group.
    """
    from django.contrib.auth.models import Group, User
    
    try:
        authorities_group = Group.objects.get(name='Authorities')
        authority_users = authorities_group.user_set.all()
        
        for user in authority_users:
            send_custom_notification(
                user.id, 
                notification_type, 
                title, 
                message
            )
    except Group.DoesNotExist:
        print("Authorities group does not exist")
    except Exception as e:
        print(f"Error notifying authorities: {e}")