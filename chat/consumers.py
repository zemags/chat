# consumers its like views in django, but asynchronously
import json

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
# every consumer have connect, disconnect, recieve

class ChatCunsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):
        #  code - error code
        pass

    def receive(self, text_data=None, bytes_data=None):
        # receive and send back this message
        json_data = json.loads(text_data)
        message = json_data['message']
        self.send(text_data=json.dumps({
            'message': message
        }))


class AsyncChatCunsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        #  code - error code
        pass

    async def receive(self, text_data=None, bytes_data=None):
        # receive and send back this message
        json_data = json.loads(text_data)
        message = json_data['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))