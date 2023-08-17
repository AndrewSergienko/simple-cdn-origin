import json
from collections import defaultdict
from pathlib import Path

from aiohttp import ClientSession, web

from src.abstract import AServersManager, AWebClient, AWebSocketManager


class WebSocketManager(AWebSocketManager):
    def __init__(self):
        self.subscribers = {}
        # Messages without subscribers.
        self.messages = defaultdict(list)

    async def send_file_status(self, status):
        # get subscribed WebSocket object by filename
        if status["file_info"]["name"] in self.subscribers:
            websocket: web.WebSocketResponse = self.subscribers[
                status["file_info"]["name"]
            ]
            await websocket.send_json(status)
        else:
            self.messages.append(status)

    async def subscribe_to_file_status(self, file_name: str, *args, **kwargs):
        self.subscribers[file_name] = kwargs["websocket"]
        if file_name in self.messages:
            for message in self.messages[file_name]:
                await kwargs["websocket"].send(message)

    async def unsubscribe_to_file_status(self, file_name):
        del self.subscribers[file_name]


class ServersManager(AServersManager):
    async def get_servers(self, root_dir: Path) -> list[dict]:
        """Get a list of servers from a JSON file."""
        with open(root_dir / "servers.json") as f:
            return json.load(f)


class WebClient(AWebClient):
    async def get_ping_to_host(self, url: str, host: str):
        async with ClientSession() as session:
            async with session.get(f"{url}/ping/?host={host}") as resp:
                if resp.status == 200:
                    resp_json = await resp.json()
                    return {"ping": resp_json["ping"], "url": url}

    async def send_download_link(self, url: str, link: str):
        async with ClientSession() as session:
            data = json.dumps({"link": link})
            async with session.post(f"{url}/files/", data=data) as resp:
                if resp.status == 200:
                    return await resp.json()
