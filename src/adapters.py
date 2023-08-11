from aiohttp import web

from src.abstract import AWebSocketManager


class WebSocketManager(AWebSocketManager):
    def __init__(self):
        self.subscribers = {}

    async def send_file_status(self, status):
        # get subscribed WebSocket object by filename
        websocket: web.WebSocketResponse = self.subscribers[status["file_info"]["name"]]
        await websocket.send_json(status)

    async def subscribe_to_file_status(self, file_name: str, *args, **kwargs):
        self.subscribers[file_name] = kwargs["websocket"]

    async def unsubscribe_to_file_status(self, file_name):
        del self.subscribers[file_name]
