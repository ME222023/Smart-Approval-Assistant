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

def trial(wait_approve=True) -> dict:
    # 获取所有的 wait_* 键并提取 task_id
    wait_tasks = [key.decode("utf-8").split('_')[-1] for key in client.keys('wait_*')]
    status = {}
    temp = {}

    for task_id in wait_tasks:
        # 获取与 task_id 关联的所有 cus_id
        cus_ids = client.lrange(f"wait_{task_id}", 0, -1)
        # 将字节类型转换为字符串
        cus_ids = [cus_id.decode('utf-8') for cus_id in cus_ids]

        # 设置 task_id 的状态
        if wait_approve:
            status[task_id] = "通过"
        else:
            status[task_id] = "不通过"

        # 更新 cus_status 字典
        for cus_id in cus_ids:
            if cus_id not in temp:
                temp[cus_id] = {task_id: status[task_id]}
            else:
                temp[cus_id][task_id] = status[task_id]

    return temp
        
            
        
def waitApproval(tasks_id: list,  admin_id: str, wait_approve = True) -> dict:
    # wait_tasks = getWait()
    wait_tasks = [key.decode("utf-8").split('_')[-1] for key in client.keys('wait_*')]
    # print(wait_tasks)
    # wait_re = reverse()
    status = {}
    temp = {}
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
            # k = wait_re.get(id)
            # k = k.decode("utf-8")
            # from_id = k.split("_")[-1]
            # cus_id = f"{from_id}"
            # print(cus_id)
            # 获取与 task_id 关联的所有 cus_id
            cus_ids = client.lrange(f"wait_{id}", 0, -1)
            # 将字节类型转换为字符串
            cus_ids = [cus_id.decode('utf-8') for cus_id in cus_ids]
            if wait_approve:
                status[id] = "通过"
                msg = approval(id)  # 通过：True
                if msg == "操作成功！":
                    client.lpop(f"wait_{id}")
                    # client.rpush(f"ok_{cus_id}",id)
                    # qw.send_text(f"任务{id}已审批通过，请注意查看。\n", [cus_id])
                    combine_str += f"已完成任务{id}的审批。\n"
                else:
                    combine_str += f"已完成任务{id}的审批，请不要重复操作。\n"
            # 批准不通过
            else:
                status[id] = "不通过"
                # qw.send_text(f"任务{id}审批不通过，请修改后再做尝试。\n", [cus_id])
                msg = approval(id, False)  # 不通过：False
                if msg == "操作成功！":
                    client.lpop(f"wait_{id}")
                    # qw.send_text(f"任务{id}审批不通过，请修改后再做尝试。\n", [cus_id])
                    combine_str += f"已完成任务{id}的审批。\n"
                else:
                    combine_str += f"已完成任务{id}的审批，请不要重复操作。\n"
            # 更新 cus_status 字典
            for cus_id in cus_ids:
                if cus_id not in temp:
                    temp[cus_id] = {id: status[id]}
                else:
                    temp[cus_id][id] = status[id]
    qw.send_text(combine_str, [admin_id])
    return temp

def generate_output(cus_status: dict):
    for cus_id, tasks in cus_status.items():
        messages = []
        for task_id, state in tasks.items():
            if state == "通过":
                messages.append(f"任务{task_id}已审批通过，请注意查看。\n")
            else:
                messages.append(f"任务{id}审批不通过，请修改后再做尝试。\n")     
        qw.send_text("\n\n".join(messages), [cus_id])

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
                # tasks_id = getWait()
                tasks_id = [key.decode("utf-8").split('_')[-1] for key in client.keys('wait_*')]
                cus_status = waitApproval(tasks_id, admin_id, False)
                generate_output（
            elif "不通过" in msg:
                waitApproval(tasks_id, admin_id, False)
            elif msg == "审批通过":
                # tasks_id = getWait()
                tasks_id = [key.decode("utf-8").split('_')[-1] for key in client.keys('wait_*')]
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

    # wait_tasks = [key.decode("utf-8").split('_')[-1] for key in client.keys('wait_*')]
    # print(wait_tasks)        
    client.rpush(f"wait_{'125'}", 'a')
    client.rpush(f"wait_{'126'}", 'a')  
    client.rpush(f"wait_{'127'}", 'b')   
    dict_ = trial(True) 
    print(dict_) 

