from celery import Celery
import redis

broker="redis://:123@10.5.5.73:16379/0"
backend="redis://:123@10.5.5.73:16379/1"

app = Celery('tasks', broker=broker, backend=backend)

wait_approval = redis.from_url(broker)
ok_approval = redis.from_url(backend)

@app.task
def add(s:str):
    while(wait_approval)
    # 将字符串按逗号分割
    parts = s.split(',')
    
    # 将分割后的字符串转换为整数
    num1 = int(parts[0])
    num2 = int(parts[1])
    
    # 进行加法运算
    result = num1 + num2
    result


