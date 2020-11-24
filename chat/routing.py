from django.conf.urls import url

from .consumers.consumers import ChatCunsumer, AsyncChatCunsumer, BaseSyncConsumer, BaseAsyncConsumer, ChatJsonCunsumer, \
    ChatAsyncJsonCunsumer, ChatCunsumerChannels, AsyncChatCunsumerChannels, AsyncChatCunsumerChannelsDB

#  list of urls for websocket work
from .consumers.own_middleware import MyMiddlewareConsumer

websocket_urls = [
    url(r'^ws/chat/$', ChatCunsumer.as_asgi()),  # url start with ws - websocket   as_asgi like as_view
    url(r'^ws/async_chat/$', AsyncChatCunsumer.as_asgi()),
    url(r'^ws/base_sync_chat/$', BaseSyncConsumer.as_asgi()),
    url(r'^ws/base_async_chat/$', BaseAsyncConsumer.as_asgi()),
    url(r'^ws/json_sync_chat/$', ChatJsonCunsumer.as_asgi()),
    url(r'^ws/json_async_chat/$', ChatAsyncJsonCunsumer.as_asgi()),

    url(r'^ws/channel_layer_sync_chat/(?P<room_name>\w+)/$', ChatCunsumerChannels.as_asgi()),  # with channel_layer
    url(r'^ws/channel_layer_async_chat/(?P<room_name>\w+)/$', AsyncChatCunsumerChannels.as_asgi()),  # with async channel_layer
    url(r'^ws/channel_layer_async_chat_db/(?P<room_name>\w+)/$', AsyncChatCunsumerChannelsDB.as_asgi()),  # with async channel_layer

    # sessions and middleware
    url(r'^ws/middleware/$', MyMiddlewareConsumer)
]