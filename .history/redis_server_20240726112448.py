import redis
import time

redis_url = "redis://:123@10.5.5.73:16379/v1"
r = redis.from_url(redis_url)
keys = r.keys()


# for k in keys:
#     print(k)

# /eep(2)
    