from src.abstract import AContext
from src.adapters import WebSocketManager


class Context(AContext):
    def __init__(self):
        self.sockets = WebSocketManager()
