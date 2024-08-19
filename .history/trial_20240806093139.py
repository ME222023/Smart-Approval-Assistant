from chat.send_app import qywx
from chat_server import *
from ruler_handle.rules import *

# # 管理员的id
# admin_ids = [
#     "17a755177f4ad1f1d99bf8042cfbb74a"
# ]
# admin = "|".join(admin_ids)

# qw = qywx()

# def checkWait(cus_id: str):
#     while True:
#         msg = r.lpop(f"wait_{cus_id}")
#         if msg:
#             qw.send_text(f"{msg}任务待审批。", [admin])


# def checkInfo(task_id: str) -> str:
#     info = combine(task_id)

#     developer = info.developer
#     taskId = info.taskId
#     taskType = info.taskType
#     taskName = info.taskName

#     formatted_fields = [
#         f"开发者: {developer}",
#         f"任务ID: {taskId}",
#         f"任务类型: {taskType}",
#         f"任务名称: {taskName}"
#     ]  

#     message = "\n".join(formatted_fields)
#     qw.send_text(message, [admin])
#     return message


if __name__ == '__main__':
    print("------------------")
    wait_keys = r.keys('wait_*')
    print(wait_keys)
    wait_tasks = []
    for key in wait_keys:
        task_ids = r.lrange(key, 0, -1)
        print(task_ids)
        wait_tasks[key.decode('utf-8')] = [task_id.decode('utf-8') for task_id in task_ids]
    print(wait_tasks)
    print(type(wait_tasks))
    # getWait()