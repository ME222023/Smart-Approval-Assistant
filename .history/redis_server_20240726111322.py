import redis

redis_url = "redis://:123@10.5.5.73:16379/v1"
r = redis.from_url(redis_url)
keys = r.keys()

for k in keys:
    # 从 Redis 列表中弹出第一个元素
    # value = r.lpop(k)
    values = r.lrange(k,0,-1)
    print(k)
    if len(values) > 0:
        print(value)
    else:
        print("error")
    print("----------------------------------------------")
    