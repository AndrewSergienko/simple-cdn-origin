import aiohttp
from aiohttp import WSCloseCode, web
from aiohttp.web_routedef import RouteDef

from src import services
from src.abstract import AContext
from src.domain import FileInfo, FileReplicatedStatus, FileSavedStatus, Server


def get_handlers(context: AContext) -> list[RouteDef]:
    handlers = Handlers(context)
    return [
        web.get("/", handlers.index),
        web.get("/ws/", handlers.websocket_handler),
    ]


class Handlers:
    def __init__(self, context: AContext):
        self.context = context

    async def index(self, request: web.Request):
        return web.Response(status=200)

    async def file_status_handler(self, request: web.Request):
        data = await request.json()

        file_info = FileInfo(data["file_name"], data["origin_url"])
        if data["type"] not in ["saved", "replicated"]:
            return web.Response(
                status=400, reason="type must be 'saved' or 'replicated'"
            )

        if data["type"] == "saved":
            server_data = data["server"]
            server = Server(server_data["name"], server_data["ip"], server_data["zone"])
            status = FileSavedStatus(file_info, data["duration"], data["time"], server)
        else:
            from_server_data = data["from_server"]
            from_server = Server(
                from_server_data["name"],
                from_server_data["ip"],
                from_server_data["zone"],
            )
            to_server_data = data["from_server"]
            to_server = Server(
                to_server_data["name"], to_server_data["ip"], to_server_data["zone"]
            )
            status = FileReplicatedStatus(
                file_info, data["duration"], data["time"], from_server, to_server
            )
        await services.send_file_status(self.context, status)

    async def websocket_handler(self, request: web.Request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        file_name = request.query.get("file_name")
        origin_file_url = request.query.get("origin_url")

        if not file_name or not origin_file_url:
            await ws.close(
                code=WSCloseCode.INVALID_TEXT,
                message=b"file_name and origin_url params is required",
            )

        file_info = FileInfo(file_name, origin_file_url)
        await services.subscribe_to_file_status(self.context, file_info, websocket=ws)

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == "close":
                    await services.unsubscribe_to_file_status(self.context, file_info)
                    await ws.close()
                else:
                    await ws.send_str(msg.data + "/answer")
            elif msg.type == aiohttp.WSMsgType.ERROR:
                await services.unsubscribe_to_file_status(self.context, file_info)
        return ws
