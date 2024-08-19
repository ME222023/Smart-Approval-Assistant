import redis
import time
import json
from LLM.assistant import get_answer
from chat.send_app import qywx
from scheduler.schedule_handle import *
from ruler_handle.rules import *


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
                data = get_answer(msg)
                try:
                    answer = json.loads(data)
                    if isinstance(answer, dict):
                        # print(answer)
                        tasks_id = answer.get('tasks_id')
                        tasks_name = answer.get('tasks_name')
                        # print(tasks_id)
                        # print(tasks_name)
                        # 通过task_id和task_name查询
                        for id in tasks_id:
                            #return_msg = extract(id)
                            return_info = combine(id)
                            return_msg = check(return_info)
                            print(return_info)
                            # 对return_msg进行一系列操作
                            # 返回审核的结果
                            # print(return_msg)
                            # return_msg = json.dumps(return_msg, ensure_ascii=False)
                            # 返回到微信客户端
                            # qw.send_text(retrurn_info, ["17a755177f4ad1f1d99bf8042cfbb74a"])  # 返回内容，用户id
                except json.JSONDecodeError:
                    print(data)

            else:
                print("message is empty.")
    time.sleep(2)
