import redis
import time
from assistant import get_answer
from send_app import qywx

redis_url = "redis://:123@10.5.5.73:16379/v1"
r = redis.from_url(redis_url)
keys = r.keys()

qw = qywx()

for k in keys:
    print(k)

while True:
    p
    for k in keys:
        k = k.decode("utf-8")
        print(k)
        # if
        

    time.sleep(2)
    