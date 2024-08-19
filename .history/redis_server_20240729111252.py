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
                msg = get_answer(msg)
                if isinstance(msg,str):
                    print(msg)
                # print(isinstance(msg, dict))
                # answer = json.loads(msg)
                # print(isinstance(answer, dict))
                # if isinstance(msg, dict):
                #     print("----------------")
                #     answer = json.loads(msg)
                #     print(answer)
                #     tasks_id = answer.get('tasks_id')
                #     tasks_name = answer.get('tasks_name')
                #     print(tasks_id)
                #     print(tasks_name)
                #     for id in tasks_id:
                #         print(task_info1(id))
                #     # print(tasks_name)
                #     # returned_string = get_answer(msg)
                #     # if returned_string:
                #     #     answer = json.loads(returned_string)
                #     #     print(answer)
                #     # else:
                #     #     print("The returned string is empty.")
                #     # test
                #     # if tasks_id is None and tasks_name is None:
                #     #     uid = k.split("_")[-1]
                #     #     qw.send_text(answer, [uid])  # 直接返回内容
                #     # elif tasks_id:
                #     #     for id in tasks_id:
                #     #         info = task_info1(id)
                #     #         print(info)   
                #     # elif tasks_name:
                #     #     for name in tasks_name:
                #     #         info = task_info2(name)                
                #     # LLM直接返回给微信客户端
                #     # uid = k.split("_")[-1]
                #     # qw.send_text(answer, [uid])  # 返回内容，用户id
                # else: 
                #     print("fail")
                #     #print(get_answer(msg))
            else:
                print("message is empty.")
    time.sleep(2)
