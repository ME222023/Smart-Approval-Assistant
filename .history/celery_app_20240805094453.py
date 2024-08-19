from celery import Celery
import redis

broker="redis://:123@10.5.5.73:16379/0"
backend="redis://:123@10.5.5.73:16379/1"

app = Celery('tasks', broker=broker, backend=backend)

wait_approval = redis.from_url(broker)
ok_approval = redis.from_url(backend)

# @app.task
# def get_message(user):
#     msg = wait_approval.lpop(user)
#     if msg:
#         msg = msg.decode("utf-8")
#     else:
#         msg = None
#     ok_approval.rpush("ok_approval", msg)

@app.task
def get_message(user):
    msg = wait_approval.lpop(user)
    if msg:
        return msg.decode("utf-8")
    else:
        return None

@app.task
def add(s:str):
    try:
        # 将字符串按逗号分割
        parts = s.split(',')
        if len(parts) != 2:
            raise ValueError("Input string must be in the format 'num1,num2'")
        
        # 将分割后的字符串转换为整数
        num1 = int(parts[0])
        num2 = int(parts[1])
        
        # 进行加法运算
        result = num1 + num2
        return result
    except Exception as e:
        return str(e)


