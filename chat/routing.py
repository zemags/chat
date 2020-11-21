from django.conf.urls import url

from .consumers import ChatCunsumer, AsyncChatCunsumer, BaseSyncConsumer

#  list of urls for websocket work
websocket_urls = [
    url(r'^ws/chat/$', ChatCunsumer.as_asgi()),  # url start with ws - websocket   as_asgi like as_view
    url(r'^ws/async_chat/$', AsyncChatCunsumer.as_asgi()),
    url(r'^ws/base_sync_chat/$', BaseSyncConsumer.as_asgi()),
]