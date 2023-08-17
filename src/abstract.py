from abc import ABC, abstractmethod
from pathlib import Path


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


class AWebClient(ABC):
    @abstractmethod
    async def get_ping_to_host(self, url: str, host: str):
        pass

    @abstractmethod
    async def send_download_link(self, url: str, host: str):
        pass


class AServersManager(ABC):
    @abstractmethod
    async def get_servers(self, root_dir: Path) -> list[dict]:
        pass


class AContext(ABC):
    sockets: AWebSocketManager
    servers: AServersManager
    web: AWebClient

    ROOT_DIR: Path
