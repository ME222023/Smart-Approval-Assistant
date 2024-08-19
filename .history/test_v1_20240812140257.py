import redis
import time
import json
import logging
from LLM.assistant import *
from chat.send_app import qywx
from scheduler.schedule_handle import *
from ruler_handle.rules import *
from utils.redis_handle import RedisClient
# from trial import checkInfo

# redis_url = "redis://:123@10.5.5.73:16379/v1"
# redis_url = "redis://:123@10.5.5.73:16379/1"
# r = redis.from_url(redis_url)

# 测试逻辑（先写死）
# cus_id = "17a755177f4ad1f1d99bf8042cfbb74a"

# 管理员的id
admin_ids = [
    "17a755177f4ad1f1d99bf8042cfbb74a",
    "1730846d950e0a5709ac2ea44138df09"
]

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

def checkInfo(task_id: str) -> str:
    """
    输入“查看”且有任务ID：
    若为待审批任务，则返回部分调度信息
    @param task_id: 查看的调度任务ID
    @return: 返回部分调度信息
    """
    message = ""
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
    if not taskId:
        message += "该任务不是待审批任务。\n可能是其他管理员审批完成或无人申请审批该任务。"
    else:
        message = "\n".join(formatted_fields)
    return message

def checkTopk(k: int = 3) -> str:
    """
    输入“查看”且没有任务ID：
    返回k个待审批任务的部分调度信息
    @param k: 默认返回待审批任务的数量
    @return: 返回部分调度信息
    """
    tasks_id = [key.decode("utf-8").split('_')[-1] for key in client.keys('waitt_*')]
     # 取前 k 个 tasks_id
    top_k_tasks_id = tasks_id[:k]
    # 输出前 k 个 tasks_id
    output = ""
    # 列表中实际有的任务
    length = len(top_k_tasks_id)
    if not tasks_id:
        output += "目前没有待审批的任务，无法查看任务详情。"
    else:
        for task_id in top_k_tasks_id:
            output += checkInfo(task_id)
            output += "\n\n"
        output += f"以上只显示了待审批队列中前{length}个任务的信息。"
    return output

# def trial(wait_approve=True) -> dict:
#     # 获取所有的 wait_* 键并提取 task_id
#     wait_tasks = [key.decode("utf-8").split('_')[-1] for key in client.keys('wait_*')]
#     status = {}
#     temp = {}

#     for task_id in wait_tasks:
#         # 获取与 task_id 关联的所有 cus_id
#         cus_ids = client.lrange(f"wait_{task_id}", 0, -1)
#         # 将字节类型转换为字符串
#         cus_ids = [cus_id.decode('utf-8') for cus_id in cus_ids]

#         # 设置 task_id 的状态
#         if wait_approve:
#             status[task_id] = "通过"
#         else:
#             status[task_id] = "不通过"

#         # 更新 cus_status 字典
#         for cus_id in cus_ids:
#             if cus_id not in temp:
#                 temp[cus_id] = {task_id: status[task_id]}
#             else:
#                 temp[cus_id][task_id] = status[task_id]

#     return temp           
        
def waitApproval(tasks_id: list = None, admin_id: str = None, wait_approve = True) -> dict:
    """
    得到的字典结构:
    {adminA_id: [{task1_id: "通过", task2_id: "不通过"}], adminB_id: [{task3_id: "通过"}]}
    @param tasks_id: 管理员请求中提取的任务ID列表
    @param admin_id: 管理员ID
    @param wait_approve: 待审批任务通过与否的判断，默认为True即通过，False即不通过
    @return: 返回待审批任务和是否通过的字典
    """
    # wait_tasks = getWait()
    wait_tasks = [key.decode("utf-8").split('_')[-1] for key in client.keys('waitt_*')]
    print("----------------------------------------")
    print(wait_tasks)
    # wait_re = reverse()
    status = {}
    temp = {}
    # keys = r_.keys("wait_*")
    combine_str = ""
    for id in tasks_id:
        if id not in wait_tasks:
            # 发送消息给admin：该任务id不存在
            qw.send_text(f"任务{id}不存在，请查看ID输入是否正确。\n", [admin_id])
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
            cus_ids = client.lrange(f"waitt_{id}", 0, -1)
            # 将字节类型转换为字符串
            cus_ids = [cus_id.decode('utf-8') for cus_id in cus_ids]
            print(cus_ids)
            if wait_approve:
                status[id] = "通过"
                approval(id)  # 通过：True
                client.delete(f"waitt_{id}")
                # client.rpush(f"ok_{cus_id}",id)
                # qw.send_text(f"任务{id}已审批通过，请注意查看。\n", [cus_id])
            # 批准不通过
            else:
                status[id] = "不通过"
                # qw.send_text(f"任务{id}审批不通过，请修改后再做尝试。\n", [cus_id])
                approval(id, False)  # 不通过：False
                client.delete(f"waitt_{id}")
                # qw.send_text(f"任务{id}审批不通过，请修改后再做尝试。\n", [cus_id])
            combine_str += f"已完成任务{id}的审批。\n"
            # 更新 cus_status 字典
            for cus_id in cus_ids:
                if cus_id not in temp:
                    temp[cus_id] = {id: status[id]}
                else:
                    temp[cus_id][id] = status[id]
    qw.send_text(combine_str, admin_ids)
    return temp

def generate_output(cus_status: dict):
    """
    根据以下字典结构中任务通过与否的结果，回复对应的用户
    {adminA_id: [{task1_id: "通过", task2_id: "不通过"}], adminB_id: [{task3_id: "通过"}]}
    @param cus_status: waitApproval函数得到的字典
    """
    for cus_id, tasks in cus_status.items():
        messages = []
        for task_id, state in tasks.items():
            if state == "通过":
                messages.append(f"任务{task_id}已审批通过，请注意查看。\n")
            else:
                messages.append(f"任务{task_id}审批不通过，请修改后再做尝试。\n")     
        qw.send_text("\n".join(messages), [cus_id])

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
# with RedisClient(redis_url="redis://:123@10.5.5.73:16379/v1") as client:
#     def adminApprove(admin_id: str, msg: str):
#         ret_msg = get_answer(msg)
#         try:
#             result = json.loads(ret_msg)
#             tasks_id = result.get('tasks_id')
#             # tasks_id = list(map(str, tasks_id))
#             print(tasks_id)
#             # 已审批的信息查询不到
#             if "查看" in msg:
#                 for id in tasks_id:
#                     checkInfo(id, admin_id)
#             elif msg == "审批不通过":
#                 # tasks_id = getWait()
#                 tasks_id = [key.decode("utf-8").split('_')[-1] for key in client.keys('wait_*')]
#                 cus_status = waitApproval(tasks_id, admin_id, False)
#                 generate_output(cus_status)
#             elif "不通过" in msg:
#                 cus_status = waitApproval(tasks_id, admin_id, False)
#                 generate_output(cus_status)
#             elif msg == "审批通过":
#                 # tasks_id = getWait()
#                 tasks_id = [key.decode("utf-8").split('_')[-1] for key in client.keys('wait_*')]
#                 cus_status = waitApproval(tasks_id, admin_id, True)
#                 generate_output(cus_status)
#             elif "通过" in msg:
#                 cus_status = waitApproval(tasks_id, admin_id, True)
#                 print(cus_status)
#                 generate_output(cus_status)
#             else:
#                 qw.send_text("不是审批信息，请管理员重新输入。\n", [admin_id])
#         except Exception as e:
#             qw.send_text("系统出现异常，请管理员进行处理。", [admin])
#     time.sleep(2)

with RedisClient(redis_url="redis://:123@10.5.5.73:16379/v1") as client:
    def adminApprove(admin_id: str, msg: str):
        reply = getType(msg)
        try:
            result = json.loads(reply)
            tasks_id = result.get('tasks_id')
            cateogry = result.get('category')
            # print(tasks_id)
            # print(cateogry)
            # tasks_id = list(map(str, tasks_id))
            # print(type(tasks_id))
            # print(cateogry)
            # 已审批的信息查询不到
            # 取到topk个任务的信息
            if cateogry == "查看":
                message = ""
                if not tasks_id or len(tasks_id) >= 10:
                    message = checkTopk(3)
                for id in tasks_id:
                    message += checkInfo(id)
                    message += "\n\n"
                qw.send_text(message, [admin_id])
            elif cateogry == "通过":
                # 提取出来的id为空：审批所有的
                if not tasks_id:
                    tasks_id = [key.decode("utf-8").split('_')[-1] for key in client.keys('waitt_*')]
                cus_status = waitApproval(tasks_id, admin_id, True)
                print(cus_status)
                generate_output(cus_status)
            elif cateogry == "不通过":
                if not tasks_id:
                    tasks_id = [key.decode("utf-8").split('_')[-1] for key in client.keys('waitt_*')]
                cus_status = waitApproval(tasks_id, admin_id, False)
                print(cus_status)
                generate_output(cus_status)
            elif cateogry == "其他":
                qw.send_text("除了输入任务ID，请输入具体操作：审批通过/审批不通过/", [admin_id])
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            qw.send_text(reply, [admin_id])            
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
    # client.rpush(f"wait_{'125'}", 'a')
    # client.rpush(f"wait_{'126'}", 'a')  
    # client.rpush(f"wait_{'127'}", 'b')   
    # dict_ = trial(True) 
    # print(dict_) 

