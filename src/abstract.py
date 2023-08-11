from abc import ABC, abstractmethod


class AWebSocketManager(ABC):
    @abstractmethod
    async def send_file_status(self, status: dict):
        pass

    @abstractmethod
    async def subscribe_to_file_status(self, file_name: str, *args, **kwargs):
        pass

    @abstractmethod
    async def unsubscribe_to_file_status(self, file_name: str):
        pass


class AContext(ABC):
    sockets: AWebSocketManager
