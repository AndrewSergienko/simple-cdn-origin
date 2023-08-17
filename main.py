from aiohttp import web

from src.context import Context
from src.routes import get_handlers


def init_app() -> web.Application:
    app = web.Application()
    context = Context()
    app.add_routes(get_handlers(context))
    return app


web.run_app(init_app())
