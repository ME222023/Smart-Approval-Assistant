import redis

redis_url = "redis://:123@10.5.5.73:16379/v1"

class RedisClient:
    def __init__(self):
        self.client = redis.Redis.from_url(redis_url)

    def __enter__(self):
        return self
    
    def __exit__(self,exc_type,exc_value,traceback):
        if exc_type is not None:
            print()