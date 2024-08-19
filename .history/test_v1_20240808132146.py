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
    # wait_keys = client.keys("ok_*")
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

def checkInfo(task_id: str, admin_id: str):
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
    qw.send_text(message, [admin_id])

def waitApproval(tasks_id: list,  admin_id: str, wait_approve = True):
    # wait_tasks = getWait()
    wait_tasks = [key.decode("utf-8").split('_')[-1] for key in client.keys('wait_*')]
    # print(wait_tasks)
    wait_re = reverse()
    # keys = r_.keys("wait_*")
    combine_str = ""
    for id in tasks_id:
        if id not in wait_tasks:
            # 发送消息给admin：该任务id不存在
            combine_str += f"任务{id}不存在，请查看ID输入是否正确。\n"
            # qw.send_text(f"任务{id}不存在，请查看ID输入是否正确。\n", [admin])
        else:
            # 批准通过
            # 发送消息给对应的用户：***任务已经通过审批，请及时查看。
            # 有cus_id
            # 要找到id对应的键名称
            k = wait_re.get(id)
            k = k.decode("utf-8")
            from_id = k.split("_")[-1]
            cus_id = f"{from_id}"
            # print(cus_id)
            if wait_approve:
                msg = approval(id)  # 通过：True
                if msg == "操作成功！":
                    client.lpop(k)
                    # client.rpush(f"ok_{cus_id}",id)
                    qw.send_text(f"任务{id}已审批通过，请注意查看。\n", [cus_id])
                    combine_str += f"已完成任务{id}的审批。\n"
                else:
                    combine_str += f"已完成任务{id}的审批，请不要重复操作。\n"
            # 批准不通过
            else:
                # qw.send_text(f"任务{id}审批不通过，请修改后再做尝试。\n", [cus_id])
                msg = approval(id, False)  # 不通过：False
                if msg == "操作成功！":
                    client.lpop(k)
                    qw.send_text(f"任务{id}审批 
                    combine_str += f"已完成任务{id}的审批。\n"
                else:
                    combine_str += f"已完成任务{id}的审批，请不要重复操作。\n"
    qw.send_text(combine_str, [admin_id])


# r_.rpush(f"wait_{123}","123")
# r_.rpush(f"wait_{234}","124")
# r_.rpush(f"wait_{345}","125")
# r_.rpush(f"wait_{456}","126")

# r_.lpop(f"wait_{123}")
# r_.lpop(f"wait_{456}")

# def adminApprove():
#     while True:
#         with RedisClient(redis_url="redis://:123@10.5.5.73:16379/v1") as client:
#             keys = client.keys("msg_*")
#             for k in keys:
#                 msg = client.lpop(k)
#                 msg = msg.decode("utf-8")
#                 # AI部分
#                 ret_msg = get_answer(msg)
#                 # print("--------------------------------------")
#                 # print(ret_msg)
#                 # print(type(ret_msg))
#                 # result = json.loads(ret_msg)
#                 # tasks_id = result.get('tasks_id')
#                 # print(tasks_id)
#                 try:
#                     result = json.loads(ret_msg)
#                     tasks_id = result.get('tasks_id')
#                     # tasks_id = list(map(str, tasks_id))
#                     print(tasks_id)
#                     if "查看" in msg:
#                         for id in tasks_id:
#                             checkInfo(id)
#                     elif msg == "不通过审批":
#                         tasks_id = getWait()
#                         waitApproval(tasks_id, False)
#                     elif "不通过" in msg:
#                         waitApproval(tasks_id, False)
#                     elif msg == "审批通过":
#                         tasks_id = getWait()
#                         waitApproval(tasks_id)
#                     elif "通过" in msg:
#                         waitApproval(tasks_id)
#                     else:

#                 except Exception as e:
#                     qw.send_text("系统出现异常，已通知管理员进行处理。", [admin])
#             time.sleep(2)
with RedisClient(redis_url="redis://:123@10.5.5.73:16379/v1") as client:
    def adminApprove(admin_id: str, msg: str):
        ret_msg = get_answer(msg)
        try:
            result = json.loads(ret_msg)
            tasks_id = result.get('tasks_id')
            # tasks_id = list(map(str, tasks_id))
            print(tasks_id)
            # 已审批的信息查询不到
            if "查看" in msg:
                for id in tasks_id:
                    checkInfo(id, admin_id)
            elif msg == "审批不通过":
                tasks_id = getWait()
                waitApproval(tasks_id, admin_id, False)
            elif "不通过" in msg:
                waitApproval(tasks_id, admin_id, False)
            elif msg == "审批通过":
                tasks_id = getWait()
                waitApproval(tasks_id, admin_id, True)
            elif "通过" in msg:
                waitApproval(tasks_id, admin_id, True)
            else:
                qw.send_text("不是审批信息，请管理员重新输入。\n", [admin_id])
        except Exception as e:
            qw.send_text("系统出现异常，请管理员进行处理。", [admin])
    time.sleep(2)


    # keys = client.keys('wait_*')
    # print(keys)
    # for k in keys:
    #     print(type(k))

#     .decode("utf-8")
#   wait_dict = {
#     ('wait_1', 'cus_101'),
#     ('wait_2', 'cus_102'),
#     ('wait_3', 'cus_103'),
#     # 更多键值对...
# }

    wait_tasks = [key.decode("utf-8").split('_')[-1] for key in client.keys('wait_*')]
    print(wait_tasks)                    