from celery import Celery
import redis

broker="redis://:123@10.5.5.73:16379/0"
backend="redis://:123@10.5.5.73:16379/1"

app = Celery('tasks', broker=broker, backend=backend)

wait_approval = redis.from_url(broker)
ok_approval = redis.from_url(backend)

@app.task
def get_message(user):
    msg = wait_approval.lpop(user)
    if msg:
        msg = msg.decode("utf-8")
    else:
        msg = None
    ok_approval.rpush("ok_approval", msg)

@app.task
d
@app.task
def add(x, y):
    return x + y


