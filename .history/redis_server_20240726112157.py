import redis
import time

redis_url = "redis://:123@10.5.5.73:16379/v1"
r = redis.from_url(redis_url)
keys = r.keys()

while True:
    for k in keys:
        if 
        # 从 Redis 列表中弹出第一个元素
        # value = r.lpop(k)
        values = r.lrange(k,0,-1)
        print(f"msg_{k}"k)
        for value in values:
            print(value.decode('utf-8'))
            r.lpop(k)   # 弹出第一个消息
    time.sleep(1)
    # if len(values) > 0:
    #     print(value)
    # else:
    #     print("error")
    print("----------------------------------------------")
    