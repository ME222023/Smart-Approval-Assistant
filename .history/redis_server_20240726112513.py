import redis
import time

redis_url = "redis://:123@10.5.5.73:16379/v1"
r = redis.from_url(redis_url)
keys = r.keys()


# for k in keys:
#     print(k)

while True:
    for k in keys:
        k = k.decode("utf-8")
        if k.startswith("msg_"):
            msg = r.lpop(k).decode("utf-8")
            print(f"用户{k}说了：{msg}")
    time.sleep(2)
    