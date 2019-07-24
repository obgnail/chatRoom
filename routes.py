import os

from aiohttp import web
from views import index,chat,msg_send,login

from settings import STATIC_DIR


def setup_routes(app):
    app.router.add_get('/', index,name='index')
    app.router.add_post('/login/', login,name='login')
    app.router.add_get('/chat/', chat,name='chat')
    app.router.add_get('/msg_send/', msg_send,name='msg_send')



def setup_static_routes(app):
    app.router.add_static('/static/', path= STATIC_DIR , name='static')


