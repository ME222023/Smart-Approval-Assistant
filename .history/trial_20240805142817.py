import redis

wait_approval = "redis://:123@10.5.5.73:16379/v2"
ok_apppral = redis.from_url("redis://:123@10.5.5.73:16379/v3")
wait_approval = redis.from_url("redis://:123@10.5.5.73:16379/v2")