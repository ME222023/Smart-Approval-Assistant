import redis
import time
import json
import logging
from LLM.assistant import *
from chat.send_app import qywx
from scheduler.schedule_handle import *
from ruler_handle.rules import *
from utils.redis_handle import RedisClient

# 测试getType
# reply = getType("查看任务12334343")
# print(reply)
# result = json.loads(reply)
# print(result)
# tasks_id = result.get('tasks_id')
# print(tasks_id)
# cateogry = result.get('category')
# print(cateogry)

# 测试redis
with RedisClient(redis_url="redis://:123@10.5.5.73:16379/v1") as client:
    keys = client.keys(waitt_