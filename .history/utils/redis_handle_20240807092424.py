import redis

redis_url = "redis://:123@10.5.5.73:16379/v1"

class RedisClient:
    def __init__(self,):
        self.client = redis.Redis.from_url(redis_url)

    def __enter__(self):
        return self.client
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()
        if exc_type is not None:
            print(f"An exception of type {exc_type} occured with value {exc_value}")
        return False

if __name__ == "__main__":
    with RedisClient() as client:
        print(client)
        print(client.keys())
