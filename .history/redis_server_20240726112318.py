import redis
import time

redis_url = "redis://:123@10.5.5.73:16379/v1"
r = redis.from_url(redis_url)
keys = r.keys()

while True:
    for k in keys:
        if k.startswith("msg_"):
            msg = r.lpop(k)
            print("用户{}说了{}")
    time.sleep(1)
    # if len(values) > 0:
    #     print(value)
    # else:
    #     print("error")
    print("----------------------------------------------")
    