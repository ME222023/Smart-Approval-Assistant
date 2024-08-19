import redis
from test import *
from chat_server import *

def adminApprove():
    while True:
        with RedisClient(redis_url="redis://:123@10.5.5.73:16379/v1") as client:
            keys = client.keys("msg_*")
            for k in keys:
                msg = client.lpop(k)
                msg = msg.decode("utf-8")
                # AI部分
                ret_msg = get_answer(msg)