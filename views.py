import hashlib
import time
from uuid import uuid4

import aiohttp
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from sqlalchemy import or_

from db import session,User,Message
from celery_app import task


def md5(data):
    salt = '125dd4sa5#dadgl6##d4!==sa41]]=11!!R441]]&asA'
    data += (salt + str(time.time()))
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


# 密码加密
def encryption(password):
    salt = 'ppnn13moddkstFeb.1st(da&sdAA=A-AAAkj**Ha^a$sda//akj;adas@)'
    password += salt
    return hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()



@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}
    # return web.Response(text='hello world')

async def register(request):
    print('////////////')
    data = await request.post()
    name     = data.get("user")
    password = encryption(data.get("password"))

    if session.query(User).filter_by(name=name).first():
        context = {'msg':'用户名已被抢注'}
        return aiohttp_jinja2.render_template('index.html',request,context)
    else:
        task.add_user.delay(name,password)
        secret_key = md5(name)
        request.app['redis'].setex(secret_key, 60*60*12, name)
        return aiohttp_jinja2.render_template('chatroom.html',request,{'name':secret_key})


async def login(request):
    data = await request.post()
    name = data['user']
    password = encryption(data['password'])

    # 如果用户名不存在或密码错误
    if not (session.query(User).filter_by(name=name).first() 
            and session.query(User).filter_by(name=name,password=password).first()):
        context = {'msg':'用户名不存在或密码错误'}
        return aiohttp_jinja2.render_template('index.html',request,context)
    else:
        secret_key = md5(name)
        request.app['redis'].setex(secret_key, 60*60*12, name)
        return aiohttp_jinja2.render_template('chatroom.html',request,{'name':secret_key})



async def chat(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    msg = await ws.receive()
    if msg.type == aiohttp.WSMsgType.TEXT:
        user = request.app['redis'].get(msg.data)
        if user:
            request.app['websockets'][user] = ws
            print(f'======== {user} 接入 ========')
            await ws.send_json({"type":0,"userlist":list(request.app['websockets'].keys()),"userid":user})

            for each_ws in request.app['websockets'].values():
                await each_ws.send_json({"type": 0, "userlist":list(request.app['websockets'].keys()),"user":None})


    # 这里的while True并不会接受通话信息,await ws.receive()是用于捕捉离线信息的
    # 也就是说这个while True理论上来讲可以删去,加上只是为了让代码更健壮
    while True:
        msg = await ws.receive()
        if msg.type == aiohttp.WSMsgType.CLOSE:
            del request.app['websockets'][user]
            print(f'======== {user} 离线 ========')

            for each_ws in request.app['websockets'].values():
                await each_ws.send_json({"type": 0, "userlist":list(request.app['websockets'].keys()),"user":None})
            return ws
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %ws.exception())
            continue
        else:
            continue


async def msg_send(request):
    data = await request.post()

    msg        = data.get("txt")
    useridto   = data.get("userto")
    useridfrom = data.get("userfrom")
    type       = data.get("type")

    # type:1表示群聊,type:0表示私聊
    # 发来{type:"0",msg:data,user:user},表示发送聊天信息，user为空表示群组消息，不为空表示要发送至的用户
    if type == "1":
        #群发
        task.add_message.delay(useridfrom,'all',msg) # 保存信息
        # 发送信息
        for each_ws in request.app['websockets'].values():
            await each_ws.send_json({"type": 1, "data": {"msg": msg, "user": useridfrom}})
    else:
        
        task.add_message.delay(useridfrom,useridto,msg) # 保存信息
        # 私聊，对方显示
        await request.app['websockets'][useridto].send_json({"type": 1, "data": {"msg": msg, "user": useridfrom}})
        # 私聊，自己显示
        await request.app['websockets'][useridfrom].send_json({"type": 1, "data": {"msg": msg, "user": useridfrom}})
    # 返回json,为了调用send函数的回调方法
    return web.json_response({})


async def anonymous(request):
    name = '匿名用户' + str(uuid4())[:8]
    secret_key = md5(name)
    request.app['redis'].setex(secret_key, 60*60*12, name)
    return aiohttp_jinja2.render_template('chatroom.html',request,{'name':secret_key})


async def history(request):
    data = await request.post()
    secret_key = data.get("userid")
    user = request.app['redis'].get(secret_key)
    message = session.query(Message).filter(or_(Message.from_user==user,Message.to_user==user)).order_by(Message.createtime).all()
    print('************************')
    print(message)
    return aiohttp_jinja2.render_template('history.html',request,{'message':message})


async def test(request):
    await set_session(request,'name','heyingliang')
    location = request.app.router['index'].url_for()
    raise web.HTTPFound(location=location)