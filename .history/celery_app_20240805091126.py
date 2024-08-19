from celery import Celery
import redis

broker="redis://:123@10.5.5.73:16379/0"
backend="redis://:123@10.5.5.73:16379/1"
user = "msg_17a755177f4ad1f1d99bf8042cfbb74a"

app = Celery('tasks', broker=broker, backend=backend)

wait_approval = redis.from_url(broker)
ok_approval = redis.from_url(backend)

@app.task
def get_message(user):
    msg = wait_approval.lpop(user)
    
    if msg:
        return msg.decode("utf-8")
    return None


@app.task
def add(x, y):
    return x + y


