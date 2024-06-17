import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, ChatMessage
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope['user'].is_authenticated:
            await self.close()
            return

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            this.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = self.scope['user']

        room = await ChatRoom.objects.get(name=self.room_name)
        await ChatMessage.objects.create(room=room, user=user, message=message)

        await this.channel_layer.group_send(
            this.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        await this.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))
