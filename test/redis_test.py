import redis

# 使用 URL 格式连接到 Redis 服务器
redis_url = "redis://:123@10.5.5.73:16379/v1"
r = redis.from_url(redis_url)

# 测试连接是否成功
try:
    r.ping()
    print("Connected to Redis!")
except redis.ConnectionError:
    print("Failed to connect to Redis.")

keys = r.keys()
for k in keys:
    print(k)