#  request by web sockets

from channels.routing import ProtocolTypeRouter, URLRouter

from chat.routing import websocket_urls


application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urls),  # websocket - protocol name, URLRouter accept url for websockets
})  #