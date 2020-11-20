from django.conf.urls import url

from .consumers import ChatCunsumer

#  list of urls for websocket work
websocket_urls = [
    url(r'^ws/chat/$', ChatCunsumer.as_asgi()),  # url start with ws - websocket   as_asgi like as_view
]