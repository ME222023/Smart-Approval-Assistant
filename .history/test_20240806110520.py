import redis
import time
import json
import logging
from LLM.assistant import get_answer
from chat.send_app import qywx
from scheduler.schedule_handle import *
from ruler_handle.rules import *
from web_api import r as r_
# from trial import checkInfo

# redis_url = "redis://:123@10.5.5.73:16379/v1"
# redis_url = "redis://:123@10.5.5.73:16379/1"
# r = redis.from_url(redis_url)

# 管理员的id
admin_ids = [
    "17a755177f4ad1f1d99bf8042cfbb74a"
]
admin = "|".join(admin_ids)

qw = qywx()

def getWait() -> list:
    # Get all keys that match the pattern "wait_*"
    wait_keys = r_.keys("wait_*")
    # Get all values from the keys that match the pattern
    wait_values = []
    for key in wait_keys:
        wait_values = r_.lrange(key, 0, -1)  # Get all values from the list
    return wait_values

def reverse() -> list:
    keys = r_.keys("wait_*")
    # 反转键值对
    reversed_kv_pairs = []
    for key in keys:
        # 获取键对应的列表中的所有值
        values = r_.lrange(key, 0, -1)
        for value in values:
            # 构造反转后的键值对
            # print(type(value))
            reversed_kv_pairs.append((value, key))
    return reversed_kv_pairs

# result = getWait()
# print(result)
# re = reverse()
# print(re)

def waitApprova(tasks_id: list, approval = True):
    wait_tasks = getWait()
    keys = r_.keys("wait_*")
    for id in tasks_id:
        if id not in wait_tasks:
            # 发送消息给admin：该任务id不存在
            qw.send_text(f"任务{id}不存在，请查看ID输入是否正确。\n", [admin])
        else:
            if approval:
                # 批准通过
                # 发送消息给对应的用户：***任务已经通过审批，请及时查看。
                # 有cus_id
                for k in keys:
                    k = k.decode("utf-8")
                    from_id = k.split("_")[-1]
                    cus_id = f"{from_id}"

                    qw.send_text(f"任务{id}已审批通过，请注意查看。\n", [cus_id])
                    approval(id)  # 通过：True

                    r_.lpop(k)
                    r_.rpush(f"ok_{cus_id}",id)
            

                