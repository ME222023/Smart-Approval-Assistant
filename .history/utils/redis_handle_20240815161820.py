import redis
from utils.config import Config

config = Config()
config.init("/home/hezp1/AI/app_weichat/config.ini")
redis_url = config.config['server']['redis_url']

class RedisClient:
    def __init__(self, redis_url):
        self.client = redis.Redis.from_url(redis_url)

    def __enter__(self):
        return self.client
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()
        if exc_type is not None:
            print(f"An exception of type {exc_type} occured with value {exc_value}")
        return False

if __name__ == "__main__":

    # with RedisClient("redis://:123@10.5.5.73:16379/v1") as client:
    with RedisClient(redis_url) as client:
        print(client.keys())
