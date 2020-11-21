from django.conf.urls import url

from .consumers import ChatCunsumer, AsyncChatCunsumer

#  list of urls for websocket work
websocket_urls = [
    url(r'^ws/chat/$', ChatCunsumer.as_asgi()),  # url start with ws - websocket   as_asgi like as_view
    url(r'^ws/achat/$', AsyncChatCunsumer.as_asgi()),
]