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
        byte_values = r_.lrange(key, 0, -1)  # Get all values from the list
        str_values = [value.decode('utf-8') for value in byte_values]
        # 将转换后的值添加到 wait_values 列表中
        wait_values.extend(str_values)
    return wait_values

def reverse() -> dict:
    keys = r_.keys("wait_*")
    # 反转键值对
    reversed_kv_pairs = {}
    for key in keys:
        # 获取键对应的列表中的所有值
        values = r_.lrange(key, 0, -1)
        for value in values:
            # 构造反转后的键值对
            # print(type(value))
            value = value.decode('utf-8')
            # print(type(key))
            # key = key.decode('utf-8')
            # Add the reversed key-value pair to the dictionary
            reversed_kv_pairs[value] = key
    return reversed_kv_pairs

def checkInfo(task_id: str):
    info = combine(task_id)

    developer = info.developer
    taskId = info.taskId
    taskType = info.taskType
    taskName = info.taskName

    formatted_fields = [
        f"开发者: {developer}",
        f"任务ID: {taskId}",
        f"任务类型: {taskType}",
        f"任务名称: {taskName}"
    ]  

    message = "\n".join(formatted_fields)
    qw.send_text(message, [admin])

def waitApproval(tasks_id: list, wait_approve = True):
    wait_tasks = getWait()
    wait_re = reverse()
    # keys = r_.keys("wait_*")
    for id in tasks_id:
        if id not in wait_tasks:
            # 发送消息给admin：该任务id不存在
            qw.send_text(f"任务{id}不存在，请查看ID输入是否正确。\n", [admin])
        else:
            # 批准通过
            # 发送消息给对应的用户：***任务已经通过审批，请及时查看。
            # 有cus_id
            # 要找到id对应的键名称
            k = wait_re.get(id)
            k = k.decode("utf-8")
            from_id = k.split("_")[-1]
            cus_id = f"{from_id}"
            print(cus_id)
            if wait_approve:
                qw.send_text(f"任务{id}已审批通过，请注意查看。\n", [cus_id])
                approval(id)  # 通过：True

                r_.lpop(k)
                r_.rpush(f"ok_{cus_id}",id)
            # 批准不通过
            else:
                qw.send_text(f"任务{id}审批不通过，请修改后再做尝试。\n", [cus_id])
                approval(id, False)  # 不通过：False
                r_.lpop(k)
                r_.rpush(f"msg_{cus_id}",id)

try:
    while True:
        keys = r_.keys()
        for k in keys:
            msg = r_.lpop(k)
            msg = msg.decode("utf-8")
            ret_msg = get_answer(msg)
            tasks_id = ret_msg.get('tasks_id')

# result = getWait()
# print(result)
# re = reverse()
# print(re)
# waitApproval(["10038971","10038969"])

            

                