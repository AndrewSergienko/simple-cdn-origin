from dataclasses import asdict

from aiohttp import web

from src.abstract import AWebSocketManager
from src.domain import FileInfo, FileSavedStatus, FileStatus


class WebSocketManager(AWebSocketManager):
    def __init__(self):
        self.subscribers = {}

    async def send_file_status(self, status: FileStatus):
        websocket: web.WebSocketResponse = self.subscribers[status.file_info.file_name]
        data = asdict(status)
        data["status"] = (
            "saved" if isinstance(status, FileSavedStatus) else "replicated"
        )
        await websocket.send_json(data)

    async def subscribe_to_file_status(self, file: FileInfo, *args, **kwargs):
        self.subscribers[file.file_name] = kwargs["websocket"]

    async def unsubscribe_to_file_status(self, websocket, file: FileInfo):
        del self.subscribers[file.file_name]
