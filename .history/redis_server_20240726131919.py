import redis
import time
from assistant import get_answer
from send_app import qywx

redis_url = "redis://:123@10.5.5.73:16379/v1"
r = redis.from_url(redis_url)
keys = r.keys()

qw = qywx()

# for k in keys:
#     print(k)

while True:
    for k in keys:
        k = k.decode("utf-8")
        if k.startswith("msg_"):
            msg = r.lpop(k)
            if msg is not None:
                msg = msg.decode("utf-8")
                print(f"用户{k}说了：{msg}")
                answer = get_answer(msg)
                uid = 
                qw.send_text(answer, ["17a755177f4ad1f1d99bf8042cfbb74a"])  # 返回内容，用户id
    time.sleep(2)
    