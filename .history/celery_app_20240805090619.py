from celery import Celery

broker="redis://:123@10.5.5.73:16379/0"
backend="redis://:123@10.5.5.73:16379/1"

app = Celery('tasks', broker="redis://:123@10.5.5.73:16379/0", backend="redis://:123@10.5.5.73:16379/1")


msg = broker.lpop(k)
msg = msg.decode("utf-8")

@app.task
def add(x, y):
    return x + y


