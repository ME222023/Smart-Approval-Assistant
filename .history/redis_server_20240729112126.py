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
            # print(msg)
            if msg is not None:
                msg = msg.decode("utf-8")
                print(f"用户{k}说了：{msg}")
                # print(isinstance(msg, dict))
                data = get_answer(msg)
                # print(isinstance(msg,str))
                # if isinstance(msg,str):
                #     print(msg)
                # else:
                #     print("fail")
                try:
                    json_data = json.loads(data)
                    if()
                except json.JSONDecodeError as e:
                    print("JSONDecodeError:", e)
                    print("Invalid JSON string:", data)
                # print(isinstance(msg, dict))
                # answer = json.loads(msg)
                # print(isinstance(answer, dict))
                
                # else: 
                #     print("fail")
                #     #print(get_answer(msg))
            else:
                print("message is empty.")
    time.sleep(2)
