import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import Chat
from api.serializers import ChatSerializer
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from rest_framework.viewsets import ModelViewSet

from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'test'

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name)

        await self.accept()
        print(self.scope['user'].username)

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        await self.save_message(username, self.room_group_name, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )
        
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        await self.send(text_data=json.dumps(
            {
                'type': 'chat',
                'message': message,
                'username': username,
            }
        ))
    
    @database_sync_to_async
    def save_message(self, username, thread_name, message):
        Chat.objects.create(
            sender=username, message=message, thread_name=thread_name)
        
class ChatAPIConsumer(ModelViewSet):

    queryset = Chat.objects.all()
    serializer_class = ChatSerializer