from celery import Celery

app = Celery('tasks', broker="redis://:123@10.5.5.73:16379/0", backend="redis://:123@10.5.5.73:16379/1")



@app.task
def add(x, y):
    return x + y


