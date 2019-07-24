import time
from celery_app import app

@app.task
def multiply(x, y):
    time.sleep(2)
    print(x * y)
    return x * y