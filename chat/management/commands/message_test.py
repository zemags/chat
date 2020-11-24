import time

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        channel_layer = get_channel_layer()  # access to channel_layer in consumer like self.channel_layer
        for i in range(10):  # 10 times send message to group chat
            async_to_sync(channel_layer.group_send)(
                'room_name',
                {
                    'type': 'chat.message.custom',
                    'text': f"message {i} outside of consumer"
                }
            )
            time.sleep(1)