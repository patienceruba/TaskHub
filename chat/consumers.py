import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from teams.models import Team
from .models import Message
from notifications.models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.team_id = self.scope['url_route']['kwargs']['team_id']
        self.room_group_name = f'team_chat_{self.team_id}'

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data.get('message', '').strip()
        user = self.scope.get('user')

        # Validate message and user
        if not message_content or not user or isinstance(user, AnonymousUser):
            await self.close()
            return

        # Save message
        message_instance = await self.save_message(user, message_content)

        # Create notifications for all team members except sender
        await self.create_notifications(message_instance)

        # Broadcast message to team
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender': user.username,
                'timestamp': timezone.now().isoformat(),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp'],
        }))

    @database_sync_to_async
    def save_message(self, user, message):
        try:
            team = Team.objects.get(id=self.team_id)
            return Message.objects.create(sender=user, team=team, content=message)
        except Team.DoesNotExist:
            return None

    @database_sync_to_async
    def create_notifications(self, message_instance):
        if not message_instance:
            return

        # Get all actual users in the team except sender
        recipients = [
            member.user 
            for member in message_instance.team.members.exclude(user=message_instance.sender)
        ]

        for user in recipients:
            notif = Notification.objects.create(
                user=user,
                message=message_instance,
                type='chat'
            )

            # Optionally send via WebSocket to each user
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}",
                {
                    "type": "send_notification",
                    "message": f"New message from {message_instance.sender.username}: {message_instance.content}",
                    "notification_id": notif.id
                }
            )
