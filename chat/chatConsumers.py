import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from teams.models import Team
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.team_id = self.scope['url_route']['kwargs']['team_id']
        self.room_group_name = f'chat_{self.team_id}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '').strip()
        user = self.scope.get('user')

        if not message or not user or isinstance(user, AnonymousUser):
            return

        await self.save_message(user, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': user.username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
        }))

    @database_sync_to_async
    def save_message(self, user, message):
        team = Team.objects.get(id=self.team_id)
        Message.objects.create(sender=user, team=team, content=message)
    

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '').strip()
        user = self.scope.get('user')
        print("Received message:", message, "from user:", user)  # Add this

        if not message or not user or isinstance(user, AnonymousUser):
            return

