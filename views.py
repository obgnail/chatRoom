import aiohttp
import aiohttp_jinja2
from aiohttp import web

from db import session,User,Message
from celery_app import task



@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}
    # return web.Response(text='hello world')

async def login(request):
    data = await request.post()
    name = data['user']
    password = data['password']

    if session.query(User).filter_by(name=name).first():
        return web.Response(text='已存在')
    else:
        task.add_user.delay(name,password)

    



async def chat(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            print('===============',msg.data)
            # if msg.data == 'close':
            #     await ws.close()
            # else:
            #     print('===============',msg.data)

                # await ws.send_str(msg.data + '/answer')
                
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %ws.exception())

    print('websocket connection closed')
    return ws



async def msg_send(request):
    pass

