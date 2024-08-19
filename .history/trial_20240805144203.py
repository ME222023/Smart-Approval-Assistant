import redis

wait_approval = redis.from_url("redis://:123@10.5.5.73:16379/v2")
ok_appproval = redis.from_url("redis://:123@10.5.5.73:16379/v3")

def checkWait(cus_id: str):
    while True:
        msg = wait_approval.lpop(f"msg_{cus_id}")
        if msg:
            