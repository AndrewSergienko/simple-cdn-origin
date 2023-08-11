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

    async def websocket_handler(self, request: web.Request):
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
