from chat.send_app import qywx
from chat_server import *
from ruler_handle.rules import *

# 管理员的id
admin_ids = [
    "17a755177f4ad1f1d99bf8042cfbb74a"
]
admin = "|".join(admin_ids)

qw = qywx()

def checkWait(cus_id: str):
    while True:
        msg = r.lpop(f"wait_{cus_id}")
        if msg:
            qw.send_text(f"{msg}任务待审批。", [admin])


def checkInfo(task_id: str) -> str:
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
    return message


if __name__ == '__main__':
    id_list = getWait()
                print(id_list)