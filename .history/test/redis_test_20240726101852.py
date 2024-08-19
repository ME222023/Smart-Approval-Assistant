import redis

# 使用 URL 格式连接到 Redis 服务器
C

# 测试连接是否成功
try:
    r.ping()
    print("Connected to Redis!")
except redis.ConnectionError:
    print("Failed to connect to Redis.")

