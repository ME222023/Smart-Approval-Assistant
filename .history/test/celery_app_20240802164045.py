from celery import Celery

app = Celery('tasks', broker="redis://:123@10.5.5.73:16379/v1")

@app.task
def add(x, y):
    return x + y
