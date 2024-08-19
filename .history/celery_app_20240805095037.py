from celery import Celery
import redis

broker="redis://:123@10.5.5.73:16379/0"
backend="redis://:123@10.5.5.73:16379/1"

app = Celery('tasks', broker=broker, backend=backend)

wait_approval = redis.from_url(broker)
ok_approval = redis.from_url(backend)

def process_messages():
    while True:
        # 从 wait_approval 列表中弹出数据
        msg = wait_approval.lpop("wait_approval")
        if not msg:
            break  # 如果没有数据，退出循环

        # 解码消息
        msg = msg.decode("utf-8")

        # 将字符串按逗号分割
        parts = msg.split(',')
        if len(parts) != 2:
            continue  # 如果格式不对，跳过该消息

        try:
            # 将分割后的字符串转换为整数
            num1 = int(parts[0])
            num2 = int(parts[1])
        except ValueError:
            continue  # 如果转换失败，跳过该消息

        # 进行加法运算
        result = num1 + num2

        # 将结果压入 ok_approval 列表中
        ok_approval.rpush("ok_approval", str(result))

# @app.task
# def get_message(user):
#     msg = wait_approval.lpop(user)
#     if msg:
#         msg = msg.decode("utf-8")
#     else:
#         msg = None
#     ok_approval.rpush("ok_approval", msg)

# @app.task
# def get_message(user):
#     msg = wait_approval.lpop(user)
#     if msg:
#         return msg.decode("utf-8")
#     else:
#         return None