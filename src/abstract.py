from abc import ABC, abstractmethod

from src.domain import FileStatus, FileInfo


class AWebSocketManager(ABC):
    @abstractmethod
    async def send_file_status(self, status: FileStatus):
        pass

    @abstractmethod
    async def subscribe_to_file_status(self, file: FileInfo, *args, **kwargs):
        pass

    @abstractmethod
    async def unsubscribe_to_file_status(self, websocket, file: FileInfo):
        pass


class AContext(ABC):
    sockets: AWebSocketManager
