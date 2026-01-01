import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Report

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the user from the scope (provided by AuthMiddlewareStack)
        self.user = self.scope["user"]
        
        if self.user.is_anonymous:
            # Reject anonymous users
            await self.close()
            return
        
        # Create a user-specific group
        self.user_group_name = f"user_{self.user.id}"
        
        # Join the user's personal group
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send connection confirmation
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected to real-time notifications',
            'user_id': self.user.id
        }))

    async def disconnect(self, close_code):
        # Leave the user's personal group
        if hasattr(self, 'user_group_name'):
            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        # Handle messages from WebSocket
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')
            
            if message_type == 'ping':
                # Respond to ping with pong
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': text_data_json.get('timestamp')
                }))
                
            elif message_type == 'get_user_stats':
                # Send current user statistics
                stats = await self.get_user_stats()
                await self.send(text_data=json.dumps({
                    'type': 'user_stats',
                    'data': stats
                }))
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))

    # Handler for report status updates
    async def report_status_update(self, event):
        # Send the status update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'report_status_update',
            'data': event['data']
        }))

    # Handler for general notifications
    async def notification(self, event):
        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'data': event['data']
        }))
    
    @database_sync_to_async
    def get_user_stats(self):
        """Get current user statistics"""
        user_reports = Report.objects.filter(user=self.user)
        return {
            'total_reports': user_reports.count(),
            'pending_reports': user_reports.filter(workflow_status='pending').count(),
            'under_review_reports': user_reports.filter(workflow_status='under_review').count(),
            'resolved_reports': user_reports.filter(workflow_status='resolved').count(),
            'rejected_reports': user_reports.filter(workflow_status='rejected').count(),
        }