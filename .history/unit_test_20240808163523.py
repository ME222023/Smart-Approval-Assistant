import redis
import time
import json
import logging
from LLM.assistant import *
from chat.send_app import qywx
from scheduler.schedule_handle import *
from ruler_handle.rules import *
from utils.redis_handle import RedisClient

reply = getType("请帮我查看10038996")
# result = json.loads(reply)
# print(result)
# tasks_id = result.get('tasks_id')
# print(tasks_id)
# cateogry = result.get('cateogry')
# print(cateogry)
