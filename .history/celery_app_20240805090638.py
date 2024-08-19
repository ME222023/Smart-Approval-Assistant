from celery import Celery

broker="redis://:123@10.5.5.73:16379/0"
backend="redis://:123@10.5.5.73:16379/1"

app = Celery('tasks', broker=broker, backend=backend)

msg = broker.lpop()
msg = msg.decode("utf-8")

@app.task
def add(x, y):
    return x + y


