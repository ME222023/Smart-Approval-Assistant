import redis
import time
from assistant import get_answer
from send_app import qywx
from task

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
                answer = get_answer(msg)
                tasks_id = answer.get('tasks_id')
                for id in tasks_id:


                # LLM直接返回给微信客户端
                # uid = k.split("_")[-1]
                # qw.send_text(answer, [uid])  # 返回内容，用户id
    time.sleep(2)
