import redis
from chat.send_app import qywx

wait_approval = redis.from_url("redis://:123@10.5.5.73:16379/v2")
ok_appproval = redis.from_url("redis://:123@10.5.5.73:16379/v3")

# 管理员的id
admin_ids = [
    "17a755177f4ad1f1d99bf8042cfbb74a"
]
admin = "|".join(admin_ids)

qw = qywx()

def checkWait(cus_id: str):
    while True:
        msg = wait_approval.lpop(f"msg_{cus_id}")
        if msg:
            qw.send_text(f"{mmsg}", [admin])
