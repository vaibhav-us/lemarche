import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Room,UserModel,Message
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user1 = self.scope['url_route']['kwargs']['user1']
        self.user2 =self.scope['url_route']['kwargs']['user2']
        self.room_name = f"{self.user1}-{self.user2}"
        
        self.room_group_name = f'chat_{self.room_name}'
        
        self.room = await self.get_or_create_room(self.user1,self.user2)
        print(f"User1: {self.user1}, User2: {self.user2}, Room: {self.room_name}")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.send(text_data=json.dumps({
            'message': 'Connection established hii',
            'user1': self.user1,
            'user2': self.user2,
            'room_name': self.room_name
        }))

        messages = await self.get_previous_messages()
        for message in messages:
            await self.send(text_data=json.dumps({
                'message': message['message'],
                'user': message['user']
            }))
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"Disconnected with code: {close_code}")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']
        await self.save_message(message,user)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        await self.send(text_data=json.dumps({
            'message': message,
            'user':user
        }))


    @sync_to_async
    def save_message(self, message,user):
        user = UserModel.objects.get(id=user)
        return Message.objects.create(message=message, room=self.room,user=user)

    @sync_to_async
    def get_previous_messages(self):
        messages = Message.objects.filter(room=self.room).order_by('id')
        return list(messages.values('message', 'user'))

        
        

    @sync_to_async
    def get_or_create_room(self, user1, user2):
        user1 = UserModel.objects.get(id=user1)
        user2 = UserModel.objects.get(id=user2)
        room,created  = Room.objects.get_or_create(user1=user1, user2=user2)
        return room
    
