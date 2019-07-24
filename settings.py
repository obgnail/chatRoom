import os

HOST = '127.0.0.1'
POST = 8080


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      # 项目路径
STATIC_DIR = os.path.join(BASE_DIR, 'websocket\static')       # 静态文件路径

# mysql
DATABASE = {
	'database' : 'aiohttpwebsocket',
	'user' : 'root',
	'password' : '5KVp2y7,k96o',
	'host' : 'localhost',
	'charset' : 'utf8',
	'echo' : True,
}


# redis
REDIS = {
	'HOST':'localhost',
	'POST':6379,
	'DB':5,
}

