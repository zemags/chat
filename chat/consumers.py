# consumers its like views in django, but asynchronously
import json

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
# every consumer have connect, disconnect, recieve

from channels.consumer import SyncConsumer

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


class BaseSyncConsumer(SyncConsumer):
    # for asgi protocol type, 'cause SyncConsumer prootocol like asgi protocol
    # and asgi have 4 type events: websocket.send, websocket.accept, websocket.receive, websocket.disconnect
    def websocket_connect(self, event):  # replace point to underscore for event like websocket_connect
        self.send({
            'type': 'websocket.accept'  # websocket.accept its event, and first item will be type
        })

    def websocket_receive(self, event):
        self.send({
            'type': 'websocket.send',
            'text': event['text']  # send back event with our text
        })