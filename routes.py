import os

from aiohttp import web
from views import index,chat,msg_send,login,test,anonymous,history,register

from settings import STATIC_DIR


def setup_routes(app):
    app.router.add_get('/', index,name='index')
    app.router.add_post('/register/', register,name='register')
    app.router.add_post('/login/', login,name='login')

    app.router.add_get('/chat/', chat,name='chat')
    app.router.add_post('/msg_send/', msg_send,name='msg_send')

    app.router.add_get('/anonymous/', anonymous,name='anonymous')
    app.router.add_post('/history/', history,name='history')


    app.router.add_get('/test', test,name='test')


def setup_static_routes(app):
    app.router.add_static('/static/', path= STATIC_DIR , name='static')


