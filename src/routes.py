import re
import socket

import aiofiles
import aiohttp
from aiohttp import WSCloseCode, web
from aiohttp.web_routedef import RouteDef

from src import services
from src.abstract import AContext


def get_handlers(context: AContext) -> list[RouteDef]:
    handlers = Handlers(context)
    return [
        web.get("/", handlers.index),
        web.get("/ws/", handlers.websocket_handler),
        web.post("/status/", handlers.file_status_handler),
        web.post("/files/", handlers.download_file_handler),
    ]


class Handlers:
    def __init__(self, context: AContext):
        self.context = context

    async def index(self, request: web.Request):
        """Return the index.html file"""
        async with aiofiles.open("index.html") as f:
            content = await f.read()
            return web.Response(text=content, content_type="text/html", status=200)

    async def file_status_handler(self, request: web.Request):
        """Processing file status and sending information to the user via WebSocket."""
        data = await request.json()

        if data["type"] not in ["saved", "replicated"]:
            reason = "type must be 'saved' or 'replicated'"
            return web.Response(status=400, reason=reason)
        await services.send_file_status(self.context, data)
        return web.Response(status=200)

    async def download_file_handler(self, request: web.Request):
        """Determine the nearest server to the file and redirect the request to it"""
        data = await request.json()
        link = data.get("link")
        if not link:
            raise web.HTTPBadRequest(text="link is required.")

        # extracting host from the URL
        host = re.search(r"^(?:https?://)?([a-zA-Z0-9.-]+)", link).groups()[0]
        # get the server with the lowest ping to a host
        servers_ping = await services.servers_ping_to_host(self.context, host)
        min_ping_server = min(servers_ping, key=servers_ping.get)
        # start the file upload to the file server
        download_file_response = await services.send_download_link(
            self.context, min_ping_server, link
        )
        return web.json_response(download_file_response, status=200)

    async def websocket_handler(self, request: web.Request):
        """
        WebSocket handler for user connection.
        Real-time updates about the uploaded file are sent over the WebSocket.
        """
        ws = web.WebSocketResponse()
        # prepare the WebSocket for connection
        await ws.prepare(request)

        file_name = request.query.get("file_name")
        origin_file_url = request.query.get("origin_url")

        if not file_name or not origin_file_url:
            code = WSCloseCode.INVALID_TEXT
            message = b"file_name and origin_url params is required"
            await ws.close(code=code, message=message)

        # subscribe the user's WebSocket object to receive file status updates
        await services.subscribe_to_file_status(self.context, file_name, websocket=ws)

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == "close":
                    # unsubscribe WebSocket object
                    await services.unsubscribe_to_file_status(self.context, file_name)
                    await ws.close()
            elif msg.type == aiohttp.WSMsgType.ERROR:
                await services.unsubscribe_to_file_status(self.context, file_name)
        return ws
