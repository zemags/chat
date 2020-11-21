# consumers its like views in django, but asynchronously
import json

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
# every consumer have connect, disconnect, recieve

from channels.consumer import SyncConsumer, AsyncConsumer

# coding and decoding cumsumver for asynchronously
from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer

from channels.exceptions import StopConsumer

class ChatCunsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        # self.close()  # close websocket its default method

    def disconnect(self, code):
        # code - error code
        pass

    def receive(self, text_data=None, bytes_data=None):

        # in class exist 'scope' its like receive in django views
        for h in self.scope['headers']:
            print('header', h[0], ' >> ', h[1], '\n**')
        print(self.scope['url_route'])
        print(self.scope['path'])

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

    def websocket_disconnect(self):  # in base consumers necessarily define disconnect
        raise StopConsumer()


class BaseAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']  # send back event with our text
        })


class ChatJsonCunsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):
        # code - error code
        pass

    def receive_json(self, content, **kwargs):
        # in content enconding\deconding json
        self.send_json(content=content)  # send back users message

    @classmethod  # redefine EncodeJson class logic
    def encode_json(cls, content):
        return super().encode_json(content)

    @classmethod  # redefine DecodeJson classes methods
    def decode_json(cls, content):
        return super().decode_json(content)


class ChatAsyncJsonCunsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        # code - error code
        pass

    async def receive_json(self, content, **kwargs):
        # in content enconding\deconding json
        await self.send_json(content=content)  # send back users message

    @classmethod  # redefine EncodeJson class logic
    async def encode_json(cls, content):
        return await super().encode_json(content)

    @classmethod  # redefine DecodeJson classes methods
    async def decode_json(cls, content):
        return await super().decode_json(content)