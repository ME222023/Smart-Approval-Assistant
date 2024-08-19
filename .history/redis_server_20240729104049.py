import redis
import time
import json
from assistant import get_answer
from send_app import qywx
from task_approval import task_info1, task_info2


redis_url = "redis://:123@10.5.5.73:16379/v1"
r = redis.from_url(redis_url)

qw = qywx()

# for k in keys:
#     print(k)

while True:
    keys = r.keys()
    for k in keys:
        k = k.decode("utf-8")
        if k.startswith("msg_"):
            msg = r.lpop(k)
            if msg is not None:
                msg = msg.decode("utf-8")
                print(f"用户{k}说了：{msg}")
                if isinstance(msg, dict):
                    

                else: 
                    print(get_answer(msg))
    time.sleep(2)
