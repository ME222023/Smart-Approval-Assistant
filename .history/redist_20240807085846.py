import redis

redis_url = "redis://:123@10.5.5.73:16379/0"
# redis_url = "redis://:123@10.5.5.73:16379/1"
r = redis.from_url(redis_url)

