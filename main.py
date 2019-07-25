import base64

import redis
import jinja2
import aiohttp_jinja2
from aiohttp import web

from db import init_redis
from routes import setup_routes,setup_static_routes
from settings import HOST,POST


async def init_app():
    app = web.Application()

    # setup Jinja2 template renderer
    aiohttp_jinja2.setup(app,loader=jinja2.FileSystemLoader(r'templates'))

    setup_routes(app)
    setup_static_routes(app)

    app['websockets'] = {}

    app.on_startup.append(init_redis)
    app.on_shutdown.append(shutdown)

    return app

async def shutdown(app):
    for ws in app['websockets'].values():
        await ws.close()
    app['websockets'].clear()


def main():
    app = init_app()
    web.run_app(app,host=HOST,port=POST)
    return app


if __name__ == '__main__':
    main()
