from pathlib import Path

from src.abstract import AContext
from src.adapters import WebSocketManager, WebClient, ServersManager


class Context(AContext):
    def __init__(self):
        self.sockets = WebSocketManager()
        self.web = WebClient()
        self.servers = ServersManager()

        self.ROOT_DIR = Path(__file__).parent.parent
