# from task1 import add_message
from celery_app import task1


if __name__ == "__main__":
    task1.add_message.delay('liangbo', 'heyingliang', 'this is content')
