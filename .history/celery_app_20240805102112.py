import redis
from celery import Celery
from chat.send_app import qywx

broker="redis://:123@10.5.5.73:16379/0"
backend="redis://:123@10.5.5.73:16379/1"
user = "msg_17a755177f4ad1f1d99bf8042cfbb74a"
app = Celery('tasks', broker=broker, backend=backend)

wait_approval = redis.from_url(broker)
ok_approval = redis.from_url(backend)

qw = qywx()

@app.task
def get_message():
    while wait_approval.lpop(user):
            msg = wait_approval.lpop(user).decode("utf-8")
            ok_approval.rpush("ok_approval", msg)
    

def print_ok_approval():
    # 获取 wait_approval 列表中的所有数据
    all_messages = ok_approval.lrange("ok_approval", 0, -1)
    
    if not all_messages:
        print("The ok_approval queue is empty.")
        return
    
    # 打印所有数据
    print("Messages in ok_approval queue:")
    for msg in all_messages:
        print(msg.decode("utf-8"))


def print_wait_approval():
    # 获取 wait_approval 列表中的所有数据
    all_messages = wait_approval.lrange("wait_approval", 0, -1)
    
    if not all_messages:
        print("The wait_approval queue is empty.")
        return
    
    # 打印所有数据
    print("Messages in wait_approval queue:")
    for msg in all_messages:
        print(msg.decode("utf-8"))

@app.task
def addMsg():
    while True:
        # 从 wait_approval 列表中弹出数据
        msg = wait_approval.lpop(user)
        print(msg)
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
        print(result)

        # 将结果压入 ok_approval 列表中
        ok_approval.rpush("ok_approval", str(result))

@app.task
def printMsg():
    while True:
        # 从 ok_approval 列表中弹出数据
        msg = ok_approval.lpop(user)
        print(msg)

        if not msg:
            break  # 如果没有数据，退出循环

        # 解码消息
        msg = msg.decode("utf-8")
        
        # 发送消息
        qw.send_text(msg, "17a755177f4ad1f1d99bf8042cfbb74a")
        



# @app.task
# def get_message(user):
#     msg = wait_approval.lpop(user)
#     if msg:
#         return msg.decode("utf-8")
#     else:
#         return None