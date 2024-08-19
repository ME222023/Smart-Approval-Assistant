import redis

wait_approval = redis.from_url("redis://:123@10.5.5.73:16379/v2")
ok_appproval = redis.from_url("redis://:123@10.5.5.73:16379/v3")

