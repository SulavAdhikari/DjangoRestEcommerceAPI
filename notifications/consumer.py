import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class NotificationConsumer(WebsocketConsumer):
    async def websocket_connect(self):
        print('connecting')
        self.room_name = self.scope['url_route']['kwargs']['user_id']
        user = self.scope['user']
        if self.room_name == user:
            async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
            )
            self.accept()
        self.reject()



    async def disconnect(self, code):
        return await self.close()


    def send(self, text_data=None, bytes_data=None, close=False):
        return super().send(text_data, bytes_data, close)
    
    def receive(self, text_data=None, bytes_data=None):
        return super().receive(text_data, bytes_data)
        
    def send_notifications(self, event):
        data = json.loads(event.get('value'))
        self.send(text_data=json.dumps({'payload':data}))
        