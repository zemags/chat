#  request by web sockets

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
from channels.auth import AuthMiddlewareStack

from chat.routing import websocket_urls


application = ProtocolTypeRouter({
    # adding session middleware
    # 'websocket': SessionMiddlewareStack(URLRouter(websocket_urls)),  # websocket - protocol name, URLRouter accept url for websockets

    # adding users middleware
    'websocket': AuthMiddlewareStack(URLRouter(websocket_urls)),  # websocket - protocol name, URLRouter accept url for websockets
})  #