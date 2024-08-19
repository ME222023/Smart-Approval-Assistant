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
    developer = info.developer
    taskId = info.taskId
    taskType = info.taskType
    taskName = info.taskName

    formatted_fields = [
        f"开发者: {developer}",
        f"任务ID: {taskId}",
        f"任务类型: {taskType}",
        f"任务名称: {taskName}"
    ]  

    message = "\n".join(formatted_fields)
    qw.send_text(message, [admin])

checkInfo()



