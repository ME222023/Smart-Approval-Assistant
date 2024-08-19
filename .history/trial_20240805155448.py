import redis
from chat.send_app import qywx
from chat_server import *
from ruler_handle.rules import *

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
        msg = wait_approval.lpop(f"wait_{cus_id}")
        if msg:
            qw.send_text(f"{msg}任务待审批。", [admin])

def checkInfo(task_id: str):
    info = combine(task_id)
    developer = info.de
    qw.send_text(info, [admin])






