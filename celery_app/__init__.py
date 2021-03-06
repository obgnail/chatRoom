from celery import Celery

app = Celery('chatroom')                            # 创建 Celery 实例
app.config_from_object('celery_app.celeryconfig')   # 通过 Celery 实例加载配置模块