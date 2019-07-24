import hashlib
from uuid import uuid4

import aiohttp
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session

from db import session,User,Message
from celery_app import task


def md5(data):
    data += 'a3dcb4d229de6fde0db5686dee47145d'
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


async def set_session(request,key,val):
   session = await get_session(request)
   session[key] = val


@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}
    # return web.Response(text='hello world')

async def register(request):
    pass


async def test(request):
    await set_session(request,'name','heyingliang')

    location = request.app.router['index'].url_for()
    raise web.HTTPFound(location=location)
    
    # return web.Response(text='hello world')
    # return 'redirect:/index' # 重定向跳转

async def login(request):
    data = await request.post()
    name = data['user']
    password = data['password']

    # 如果用户名不存在或密码错误
    if not (session.query(User).filter_by(name=name).first() 
            and session.query(User).filter_by(name=name,password=password).first()):
        resp = {'status':0}
        return web.json_response(resp)
    else:
        await set_session(request,'id',md5(name))
        resp = {'status':1}
        return web.json_response(resp)
        # return aiohttp_jinja2.render_template('chatroom.html',request,{})

        # task.add_user.delay(name,password)


async def chat(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    is_first_connect = True

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if is_first_connect:
                msg.data == 'connect'
                print('===============',msg.data)
                # request.websocket.send(json.dumps({"type":0,"userlist":list(clients.keys()),"userid":userid}).encode("'utf-8'"))
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                break
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

