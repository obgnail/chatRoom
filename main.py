import base64

import redis
import jinja2
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet

from db import init_redis
from routes import setup_routes,setup_static_routes
from settings import HOST,POST


async def init_app():
    app = web.Application()

    # setup Jinja2 template renderer
    aiohttp_jinja2.setup(app,loader=jinja2.FileSystemLoader(r'templates'))

    setup_routes(app)
    setup_static_routes(app)

    app.on_startup.append(init_redis)

    # 设置secret_key
    fernet_key = fernet.Fernet.generate_key()
    # secret_key必须是32位的url安全的经过base64编码的字节
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))

    return app

def main():
    app = init_app()
    web.run_app(app,host=HOST,port=POST)
    return app


app = main()
