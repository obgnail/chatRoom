import hashlib
import time
from uuid import uuid4

import aiohttp
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session

from db import session,User,Message
from celery_app import task


def md5(data):
    data += ('a3dcb4d229de6fde0db5686dee47145d' + str(time.time()))
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()



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


async def login(request):
    data = await request.post()
    name = data['user']
    password = data['password']

    # 如果用户名不存在或密码错误
    if not (session.query(User).filter_by(name=name).first() 
            and session.query(User).filter_by(name=name,password=password).first()):
        context = {'msg':'用户名不存在或密码错误'}
        return aiohttp_jinja2.render_template('index.html',request,context)
    else:
        secret_key = md5(name)
        request.app['redis'].setex(secret_key, 60*60*12, name)
        return aiohttp_jinja2.render_template('chatroom.html',request,{'name':secret_key})

        # task.add_user.delay(name,password)


async def chat(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            user = request.app['redis'].get(msg.data)
            if user:
                request.app['websockets'][user] = ws
                print(f'======== {user} 连接成功 ========')
                await ws.send_json({"type":0,"userlist":list(request.app['websockets'].keys()),"userid":user})

                for each_ws in request.app['websockets'].values():
                    await each_ws.send_json({"type": 0, "userlist":list(request.app['websockets'].keys()),"user":None})

        elif msg.type == aiohttp.WSMsgType.CLOSED:
            print(f'======== {user} 离线 ========')
            del request.app['websockets'][user]

            for each_ws in request.app['websockets'].values():
                await each_ws.send_json({"type": 0, "userlist":list(request.app['websockets'].keys()),"user":None})
            await ws.close()

        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %ws.exception())

    print('websocket connection closed')
    return ws


async def msg_send(request):
    data = await request.post()

    msg        = data.get("txt")
    useridto   = data.get("userto")
    useridfrom = data.get("userfrom")
    type       = data.get("type")

    print('////////////',msg,useridto,useridfrom,type)
    print(request.app['websockets'])

    # type:1表示群聊,type:0表示私聊
    # 发来{type:"0",msg:data,user:user},表示发送聊天信息，user为空表示群组消息，不为空表示要发送至的用户
    if type == "1":
        #群发
        for each_ws in request.app['websockets'].values():
            await each_ws.send_json({"type": 1, "data": {"msg": msg, "user": useridfrom}})
    else:
        # 私聊，对方显示
        await request.app['websockets'][useridto].send_json({"type": 1, "data": {"msg": msg, "user": useridfrom}})
        # 私聊，自己显示
        await request.app['websockets'][useridfrom].send_json({"type": 1, "data": {"msg": msg, "user": useridfrom}})
