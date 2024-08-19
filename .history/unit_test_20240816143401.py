import redis
import time
import json
import logging
from LLM.assistant import *
from chat.send_app import qywx
from scheduler.schedule_handle import *
from ruler_handle.rules import *
from utils.redis_handle import RedisClient
from interact.admin_interact import *
from cus_interact import *

# 测试getType
# reply = getType("你好")
# print(reply)

# result = json.loads(reply)
# print(result)
# tasks_id = result.get('tasks_id')
# print(tasks_id)
# cateogry = result.get('category')
# print(cateogry)

# 测试redis
# with RedisClient(redis_url="redis://:123@10.5.5.73:16379/v1") as client:
#     wait_tasks = [key.decode("utf-8").split('_')[-1] for key in client.keys('waitt_*')]
#     print("----------------------------------------")
#     print(wait_tasks)
#     for id in wait_tasks:
#         cus_ids = client.lrange(f"waitt_{id}", 0, -1)
#         # 将字节类型转换为字符串
#         cus_ids = [cus_id.decode('utf-8') for cus_id in cus_ids]
#         print("--------------------------")
#         print(cus_ids)
    # for k in keys:
    #         cus_ids = client.lrange(f"waitt_{id}", 0, -1)
    #         # 将字节类型转换为字符串
    #         cus_ids = [cus_id.decode('utf-8') for cus_id in cus_ids]
    #         print(cus_ids)

# 测试：函数参数为空时函数体执行情况
# dict = None
# print(dict)
# dict = {}
# print(dict)
# str = getData(b'')
# print(str)

    # wait_tasks = [key.decode("utf-8").split('_')[-1] for key in client.keys('waitt_*')]
    # print("----------------------------------------")
    # print(wait_tasks)