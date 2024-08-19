import redis
import time
import json
import logging
from LLM.assistant import get_answer
from chat.send_app import qywx
from scheduler.schedule_handle import *
from ruler_handle.rules import *
from utils.redis_handle import RedisClient
# from trial import checkInfo

# redis_url = "redis://:123@10.5.5.73:16379/v1"
# redis_url = "redis://:123@10.5.5.73:16379/1"
# r = redis.from_url(redis_url)

# 测试逻辑（先写死）
cus_id = "17a755177f4ad1f1d99bf8042cfbb74a"

# 管理员的id
admin_ids = [
    "17a755177f4ad1f1d99bf8042cfbb74a"
]
admin = "|".join(admin_ids)

qw = qywx()

# 创建一个日志记录器
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # 设置最低日志级别为DEBUG

# 创建一个日志处理器，输出到文件
file_handler = logging.FileHandler('my_log.log')
file_handler.setLevel(logging.DEBUG)

# 创建一个日志处理器，输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 创建一个日志格式器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 将格式器添加到处理器
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 将处理器添加到记录器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def getWait() -> list:
    # Get all keys that match the pattern "wait_*"
    wait_keys = client.keys("wait_*")
    # Get all values from the keys that match the pattern
    wait_values = []
    for key in wait_keys:
        byte_values = client.lrange(key, 0, -1)  # Get all values from the list
        str_values = [value.decode('utf-8') for value in byte_values]
        # 将转换后的值添加到 wait_values 列表中
        wait_values.extend(str_values)
        # wait_values.extend(byte_values)
    return wait_values

def reverse() -> dict:
    keys = client.keys("wait_*")
    # 反转键值对
    reversed_kv_pairs = {}
    for key in keys:
        # 获取键对应的列表中的所有值
        values = client.lrange(key, 0, -1)
        for value in values:
            # 构造反转后的键值对
            # print(type(value))
            value = value.decode('utf-8')
            # print(type(key))
            # key = key.decode('utf-8')
            # Add the reversed key-value pair to the dictionary
            reversed_kv_pairs[value] = key
    return reversed_kv_pairs

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

def waitApproval(tasks_id: list, wait_approve = True):
    wait_tasks = getWait()
    print(wait_tasks)
    wait_re = reverse()
    # keys = r_.keys("wait_*")
    for id in tasks_id:
        if id not in wait_tasks:
            # 发送消息给admin：该任务id不存在
            qw.send_text(f"任务{id}不存在，请查看ID输入是否正确。\n", [admin])
        else:
            # 批准通过
            # 发送消息给对应的用户：***任务已经通过审批，请及时查看。
            # 有cus_id
            # 要找到id对应的键名称
            k = wait_re.get(id)
            k = k.decode("utf-8")
            from_id = k.split("_")[-1]
            cus_id = f"{from_id}"
            print(cus_id)
            if wait_approve:
                qw.send_text(f"任务{id}已审批通过，请注意查看。\n", [cus_id])
                approval(id)  # 通过：True

                client.lpop(k)
                client.rpush(f"ok_{cus_id}",id)
            # 批准不通过
            else:
                qw.send_text(f"任务{id}审批不通过，请修改后再做尝试。\n", [cus_id])
                approval(id, False)  # 不通过：False
                client.lpop(k)
                # r_.rpush(f"msg_{cus_id}",id)


# r_.rpush(f"wait_{123}","123")
# r_.rpush(f"wait_{234}","124")
# r_.rpush(f"wait_{345}","125")
# r_.rpush(f"wait_{456}","126")

# r_.lpop(f"wait_{123}")
# r_.lpop(f"wait_{456}")

# while True:
#     with RedisClient(redis_url="redis://:123@10.5.5.73:16379/v1") as client:
#         keys = client.keys("msg_*")
#         for k in keys:
#             msg = client.lpop(k)
#             msg = msg.decode("utf-8")
#             # AI部分
#             ret_msg = get_answer(msg)
#             # print("--------------------------------------")
#             # print(ret_msg)
#             # print(type(ret_msg))
#             # result = json.loads(ret_msg)
#             # tasks_id = result.get('tasks_id')
#             # print(tasks_id)
#             try:
#                 result = json.loads(ret_msg)
#                 tasks_id = result.get('tasks_id')
#                 # tasks_id = list(map(str, tasks_id))
#                 print(tasks_id)
#                 if "查看" in msg:
#                     for id in tasks_id:
#                         checkInfo(id)
#                 elif msg == "审批通过":
#                     tasks_id = getWait()
#                     waitApproval(tasks_id)
#                 elif "通过" in msg:
#                     waitApproval(tasks_id)
#                 elif msg == "不通过审批":
#                     tasks_id = getWait()
#                     waitApproval(tasks_id, False)
#                 elif "不通过" in msg:
#                     waitApproval(tasks_id, False)
#             except Exception as e:
#                 qw.send_text("系统出现异常，已通知管理员进行处理。", [admin])
#         time.sleep(2)

# try:
#     while True:
#         keys = r_.keys("msg_*")
#         for k in keys:
#             k = k.decode("utf-8")
#             if not k.startswith("msg_"):
#                 continue
#             # 用户的id信息
#             from_id = k.split("_")[-1]
#             cus_id = f"{from_id}"
#             answer = getData(k)
#             # print(answer)
#             # print(cus_id)
#             try:
#                 result = json.loads(answer)
#                 tasks_id = result.get('tasks_id')
#                 # print(type(tasks_id))
#                 # print(tasks_id)
#                 combined_msgs = checkId(tasks_id, cus_id)
#                 # print(combined_msgs)
#                 # print("------------------------------------------------")
#                 # id_list = getWait()
#                 # print(id_list)
#                 # print(combined_msgs)
#                 # 请帮我审批10038968和10038968两个任务
#                 # if "问题" in combined_msgs:
#                 # f"{from_id}"
#                 qw.send_text("\n\n".join(combined_msgs), [cus_id])  
#             except json.JSONDecodeError as e:
#                 logger.error(f"JSON decode error: {e}")
#                 qw.send_text(answer, [cus_id])
#             except PermissionError as e:
#                 logger.error(f"PermissionError: {e}")
#                 qw.send_text("用户没有权限，已通知管理员进行处理。", [admin])
#             except MemoryError as e:
#                 logger.critical(f"MemoryError: {e}")
#                 qw.send_text("发生了内存错误，已通知管理员进行处理。", [admin])
#             except SystemExit as e:
#                 logger.critical(f"SystemExit: {e}")
#                 qw.send_text("发生了系统退出，已通知管理员进行处理。", [admin])
#             except KeyboardInterrupt as e:
#                 logger.critical(f"KeyboardInterrupt: {e}")
#                 qw.send_text("发生了键盘中断，已通知管理员进行处理。", [admin])
#             except Exception as e:
#                 logger.critical(f"Unexpected error: {e}")
#                 qw.send_text("系统出现异常，已通知管理员进行处理。", [admin])
#         time.sleep(2)
# finally:
#     r.shutdown()

result = getWait()
print(result)
# re = reverse()
# print(re)
# waitApproval(["10038971","10038969"])

            

                