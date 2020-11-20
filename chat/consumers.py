# consumers its like views in django, but asynchronously
import json

from channels.generic.websocket import WebsocketConsumer
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