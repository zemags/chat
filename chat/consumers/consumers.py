# consumers its like views in django, but asynchronously
import json

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
# every consumer have connect, disconnect, recieve

from channels.consumer import SyncConsumer, AsyncConsumer

# coding and decoding cumsumer for asynchronously
from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer

from channels.exceptions import StopConsumer

from asgiref.sync import async_to_sync  # for sync consumers

class ChatCunsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        # self.close()  # close websocket its default method

    def disconnect(self, code):
        # code - error code
        pass

    def receive(self, text_data=None, bytes_data=None):

        # in class exist 'scope' its like request in django views
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
        raise StopConsumer()  # and necessarily call raise with stop


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


class ChatCunsumerChannels(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'] # from url get room_name
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)  # add user to chat self.room_name
        self.accept()
        # self.close()  # close websocket its default method

    def disconnect(self, code):
        # code - error code
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)
        pass

    def receive(self, text_data=None, bytes_data=None):
        async_to_sync(self.channel_layer.group_send)(  # send to all users
            self.room_name,
            {
                'type': 'chat.message',  # need to create method where can work with this type chat_message
                'text': text_data

            }
        )

    def chat_message(self, event):  # from type chat.message above
        self.send(text_data=event['text'])  # from receive


class AsyncChatCunsumerChannels(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        #  code - error code
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat.message.custom',
                'text': text_data
            }
        )

    async def chat_message_custom(self, event):  # event its dictionary above from recieve method
        # create handler
        await self.send(text_data=event['text'])


# ----- WORKING WITH DB -----

from channels.db import database_sync_to_async
from chat.models import Online

class AsyncChatCunsumerChannelsDB(AsyncWebsocketConsumer):
    async def connect(self):

        #await database_sync_to_async(self.create_online())() can call like this of like decorator
        await self.create_online()  # if use decorator database_sync_to_async
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        #  code - error code
        await self.delete_online()
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        await self.refresh_online()
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat.message.custom',
                # 'text': text_data
                'text': self.online.name  # send back channel name like: "specific.10b13bdcd26243718683549c9d9f1"
            }
        )

    async def chat_message_custom(self, event):  # event its dictionary above from recieve method
        # create handler
        await self.send(text_data=event['text'])

    # adding sync methods for work with DB
    @database_sync_to_async
    def create_online(self):
        new, _ = Online.objects.get_or_create(name=self.channel_name)  # create in db
        self.online = new  # make own attributes, this attribute exist in memory of consumer

    @database_sync_to_async
    def delete_online(self):
        Online.objects.filter(name=self.channel_name).delete()

    @database_sync_to_async
    def refresh_online(self):
        self.online.refresh_from_db()  # attribute slef.online keep in cunsumer memory, so if we change name in db, its necessarily refresh again from db


# working with session

from channels.auth import login, logout
from django.contrib.auth import get_user_model

class AsyncChatCunsumerChannelsDB(AsyncWebsocketConsumer):
    async def connect(self):

        #await database_sync_to_async(self.create_online())() can call like this of like decorator
        await self.create_online()  # if use decorator database_sync_to_async

        user = await self.get_user_from_db()
        await login(self.scope, user)
        await database_sync_to_async(self.scope['session'].save)()  # save session to db

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(self.room_name, self.channel_name)

        self.scope['session']['my_var'] = 'hello session var'  # write to session var, its saved in memory
        await database_sync_to_async(self.scope['session'].save)()  # save var for session in db, its save var after consumer died

        await self.accept()

    async def disconnect(self, code):
        #  code - error code
        await self.delete_online()
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):

        # await logout(self.scope)  #
        # await database_sync_to_async(self.scope['session'].save)()  # save session to db
        # print(self.scope['user'])  # wait anonym user

        await self.refresh_online()
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat.message.custom',
                # 'text': text_data
                #'text': self.online.name  # send back channel name like: "specific.10b13bdcd26243718683549c9d9f1"
                # 'text': self.scope['session']['my_var']  # send back var from session
                'text': text_data  # testing login session save
            }
        )

    async def chat_message_custom(self, event):  # event its dictionary above from recieve method
        # create handler
        await self.send(text_data=event['text'])

    # adding sync methods for work with DB
    @database_sync_to_async
    def create_online(self):
        new, _ = Online.objects.get_or_create(name=self.channel_name)  # create in db
        self.online = new  # make own attributes, this attribute exist in memory of consumer

    @database_sync_to_async
    def delete_online(self):
        Online.objects.filter(name=self.channel_name).delete()

    @database_sync_to_async
    def refresh_online(self):
        self.online.refresh_from_db()  # attribute slef.online keep in cunsumer memory, so if we change name in db, its necessarily refresh again from db

    @database_sync_to_async
    def get_user_from_db(self):
        # for test login logout lets get user from db
        return get_user_model().objects.filter(email='admin@admin.com').first()