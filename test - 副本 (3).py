
    # async for msg in ws:
    #     if msg.type == aiohttp.WSMsgType.TEXT:
    #         user = request.app['redis'].get(msg.data)
    #         if user:
    #             request.app['websockets'][user] = ws
    #             print(f'======== {user} 连接成功 ========')
    #             await ws.send_json({"type":0,"userlist":list(request.app['websockets'].keys()),"userid":user})

    #             for each_ws in request.app['websockets'].values():
    #                 await each_ws.send_json({"type": 0, "userlist":list(request.app['websockets'].keys()),"user":None})

    #     elif msg.type == aiohttp.WSMsgType.CLOSED:
    #         print(f'======== {user} 离线 ========')
    #         del request.app['websockets'][user]

    #         for each_ws in request.app['websockets'].values():
    #             await each_ws.send_json({"type": 0, "userlist":list(request.app['websockets'].keys()),"user":None})
    #         await ws.close()

    #     elif msg.type == aiohttp.WSMsgType.ERROR:
    #         print('ws connection closed with exception %s' %ws.exception())

    # print('websocket connection closed')
    # return ws
