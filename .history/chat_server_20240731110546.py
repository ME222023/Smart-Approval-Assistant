import redis
import time
import json
from LLM.assistant import get_answer
from chat.send_app import qywx
from scheduler.schedule_handle import *


redis_url = "redis://:123@10.5.5.73:16379/v1"
r = redis.from_url(redis_url)

qw = qywx()

# for k in keys:
#     print(k)

while True:
    print("----------------------------------")
    keys = r.keys()
    for k in keys:
        k = k.decode("utf-8")
        if k.startswith("msg_"):
            msg = r.lpop(k)
            if msg is not None:
                msg = msg.decode("utf-8")
                print(f"用户{k}说了：{msg}")
                data = get_answer(msg)
                try:
                    answer = json.loads(data)
                    if isinstance(answer, dict):
                        # print(answer)
                        tasks_id = answer.get('tasks_id')
                        tasks_name = answer.get('tasks_name')
                        print(tasks_id)
                        print(tasks_name)
                        # 通过task_id和task_name查询
请帮我审批数据生产市场下的id号为11234-11237的任务
                except json.JSONDecodeError:
                    print(data)

            else:
                print("message is empty.")
    time.sleep(2)
