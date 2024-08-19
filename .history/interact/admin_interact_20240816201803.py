import redis
import re
import time
import json
import logging
from LLM.assistant import getIdType, getName
from chat.send_app import qywx
from scheduler.schedule_handle import getLatestTaskInfo, approval
from utils.redis_handle import RedisClient
from utils.log_handle import server_log
from utils.config import Config
from collections import defaultdict

config = Config()
config.init("/home/hezp1/AI/app_weichat/config.ini")

redis_url = config.config['server']['redis_url']
admin_ids = config.config['server']['admin_ids']

# test：u_id <--> name
cusId2cusName = {
    '16bd52abceae57867cfaa7e4bb9adab4' : 'zhangxs1',
    '17369c736ab9e12dd4c5fb94e338ff78' : 'gongwj'
}
cusName2cusId = {
    'zhangxs1' : '16bd52abceae57867cfaa7e4bb9adab4',
    'gongwj' : '17369c736ab9e12dd4c5fb94e338ff78' 
}

qw = qywx()

# logger = logging.getLogger()

# logger = server_log()

def getCusIds() -> list:
    # Get all keys that match the pattern "wait_*"
    with RedisClient(redis_url) as client: 
        wait_keys = client.keys("waitt_*")
    # wait_keys = client.keys("ok_*")
    # Get all values from the keys that match the pattern
    wait_values = []
    for key in wait_keys:
        with RedisClient(redis_url) as client: 
            byte_values = client.lrange(key, 0, -1)  # Get all values from the list
        str_values = [value.decode('utf-8') for value in byte_values]
        # 将转换后的值添加到 wait_values 列表中
        wait_values.extend(str_values)
        # wait_values.extend(byte_values)
    return wait_values

def getCusNameList() -> list:
    wait_values = getCusIds()
    cus_list = []
    cus_set = set()  # 使用集合来避免重复
    for u_id in wait_values:
            if u_id in cusId2cusName:
                cus_set.add(cusId2cusName[u_id])
            else:
                print(f"User ID {u_id} not found in cus_dict")
    cus_list = list(cus_set)  # 将集合转换为列表
    return cus_list

def getReverseDict() -> dict:
    with RedisClient(redis_url) as client: 
        keys = client.keys("waitt_*")
    # 反转键值对
    reversed_kv_pairs = defaultdict(list)
    for key in keys:
        # 获取键对应的列表中的所有值
        with RedisClient(redis_url) as client: 
            values = client.lrange(key, 0, -1)
        for value in values:
            value = value.decode('utf-8')
            reversed_kv_pairs[value].append(key.decode('utf-8').replace('waitt_', ''))
    return reversed_kv_pairs

def getTaskIdsByUid(reversed_dict, u_name) -> list:
    if u_name in cusName2cusId:
        # 如果u_name不能成功转换成u_id
        u_id = cusName2cusId[u_name]
        if u_id in reversed_dict:
        # 去掉 'waitt_' 前缀并返回任务ID列表
            return [task_id for task_id in reversed_dict[u_id]]
        else:
            # 如果 u_id 不存在于字典中，返回空列表
            return []
    else:
        return []

def updateTaskStatus(reversed_kv_pairs, u_id, status):
    if u_id in reversed_kv_pairs:
        task_list = reversed_kv_pairs[u_id]
        updated_tasks = {task_id: status for task_id in task_list}
        return updated_tasks
    else:
        print(f"u_id '{u_id}' does not exist in the dictionary.")
        return {}

def viewInfo(task_id: str) -> str:
    """
    输入“查看”且有任务ID：
    若为待审批任务，则返回部分调度信息
    @param task_id: 查看的调度任务ID
    @return: 返回部分调度信息
    """
    logger.debug(f"检查任务信息，任务ID: {task_id}")
    message = ""
    try:
        info = getLatestTaskInfo(task_id)
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
            message += f"任务{task_id}不是待审批任务。\n其他管理员已经完成审批或无人申请审批该任务。"
            logger.info(f"任务ID {task_id} 不是待审批任务。")
        else:
            message = "\n".join(formatted_fields)
            logger.info(f"任务信息: {message}")
    except Exception as e:
        logger.error(f"检查任务信息失败，任务ID: {task_id}, 错误: {e}")
        message += "检查待审批任务信息时发生错误，请确保输入了正确的任务ID或用户名。"
    return message

def viewTopk(k: int = 3) -> str:
    """
    输入“查看”且没有任务ID：
    返回k个待审批任务的部分调度信息
    @param k: 默认返回待审批任务的数量
    @return: 返回部分调度信息
    """
    logger.debug(f"检查前 {k} 个待审批任务信息")
    output = ""
    try:
        tasks_id = getTasksID()
        logger.debug(f"tasks_id={tasks_id}")
        # tasks_id = [key.decode("utf-8").split('_')[-1] for key in client.keys('waitt_*')]
        # 取前 k 个 tasks_id
        top_k_tasks_id = tasks_id[:k]
        # 列表中实际有的任务
        length = len(top_k_tasks_id)
        if not tasks_id:
            output += "待审批任务列表为空，暂时没有可以查看详情的任务。"
            logger.info("目前没有待审批的任务。")
        else:
            for task_id in top_k_tasks_id:
                output += viewInfo(task_id)
                output += "\n\n"
            output += f"以上只显示了待审批队列中前{length}个任务的信息。"
            logger.info(f"显示了待审批队列中前 {length} 个任务的信息。")
    except Exception as e:
        logger.error(f"检查待审批任务信息失败，错误: {e}")
        output += "检查待审批任务信息时发生错误，请确保输入了正确的任务ID或用户名。"
    return output

 
def getTasksID() -> list:
    with RedisClient(redis_url) as client: 
        tasks_id = [key.decode("utf-8").split('_')[-1] for key in client.keys('waitt_*')]
    return tasks_id


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

     
def pendApprovalList(tasks_id: list, admin_id: str, wait_approve = True) -> dict:
    """
    得到的字典结构:
    {adminA_id: [{task1_id: "通过", task2_id: "不通过"}], adminB_id: [{task3_id: "通过"}]}
    @param tasks_id: 管理员请求中提取的任务ID列表
    @param admin_id: 管理员ID
    @param wait_approve: 待审批任务通过与否的判断，默认为True即通过，False即不通过
    @return: 返回待审批任务和是否通过的字典
    """
    # wait_tasks = getWait()
    logger.debug(f"管理员 {admin_id} 请求审批任务: {tasks_id}, 审批状态: {'通过' if wait_approve else '不通过'}")
    # wait_tasks = [key.decode("utf-8").split('_')[-1] for key in client.keys('waitt_*')]
    wait_tasks = getTasksID()
    if not wait_tasks:
        logger.info(f"待审批任务列表为空，管理员 {admin_id} 无任务可审批。")
        qw.send_text("待审批任务列表为空，暂时没有可以审批的任务。\n", [admin_id])
        return {}
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
            logger.warning(f"任务 {id} 不存在，管理员 {admin_id} 输入错误。")
            qw.send_text(f"任务{id}不存在，请查看ID输入是否正确。\n", [admin_id])
            return {}
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
            with RedisClient(redis_url) as client:   
                cus_ids = client.lrange(f"waitt_{id}", 0, -1)
            # 将字节类型转换为字符串
            cus_ids = [cus_id.decode('utf-8') for cus_id in cus_ids]
            logger.debug(f"任务 {id} 关联的用户ID: {cus_ids}")
            # print(cus_ids)
            if wait_approve:
                status[id] = "通过"
                approval(id)  # 通过：True
                # ----------------test--------------------------
                with RedisClient(redis_url) as client:   
                    client.delete(f"waitt_{id}")
                logger.info(f"任务 {id} 已审批通过。")
                # client.rpush(f"ok_{cus_id}",id)
                # qw.send_text(f"任务{id}已审批通过，请注意查看。\n", [cus_id])
            # 批准不通过
            else:
                status[id] = "不通过"
                # qw.send_text(f"任务{id}审批不通过，请修改后再做尝试。\n", [cus_id])
                approval(id, False)  # 不通过：False
                with RedisClient(redis_url) as client:   
                    client.delete(f"waitt_{id}")
                logger.info(f"任务 {id} 审批不通过。")
                # qw.send_text(f"任务{id}审批不通过，请修改后再做尝试。\n", [cus_id])
            combine_str += f"已完成任务{id}的审批。\n"
            # 更新 cus_status 字典
            for cus_id in cus_ids:
                if cus_id not in temp:
                    temp[cus_id] = {id: status[id]}
                else:
                    temp[cus_id][id] = status[id]
    qw.send_text(combine_str, [admin_ids])
    return temp

def printAprroval(cus_status: dict = {}):
    """
    根据以下字典结构中任务通过与否的结果，回复对应的用户
    {adminA_id: [{task1_id: "通过", task2_id: "不通过"}], adminB_id: [{task3_id: "通过"}]}
    @param cus_status: waitApproval函数得到的字典
    """
    logger.debug(f"生成输出，用户任务状态: {cus_status}")
    for cus_id, tasks in cus_status.items():
        messages = []
        for task_id, state in tasks.items():
            if state == "通过":
                messages.append(f"任务{task_id}已审批通过，请注意查看。\n")
            else:
                messages.append(f"任务{task_id}审批不通过，请修改后再做尝试。\n")     
        qw.send_text("\n".join(messages), [cus_id])

def getTaskListByCus(cus_status: dict, cus_name: str):
    cus_id = cusName2cusId[cus_name]
    if cus_id and cus_id in cus_status:
        task_list = []
        for task_dict in cus_status[cus_id]:
            task_list.extend(task_dict.keys())
        qw.send_text("\n".join(task_list), [cus_id])
    else:
        print(f"Admin ID {cus_id} not found in cus_status")

def adminInteract(admin_id: str, msg: str):
    logger.debug(f"管理员 {admin_id} 收到消息: {msg}")
    # -----------------新增需求-----------------------
    pattern = r"查看待审批用户"
    if re.search(pattern, msg):
        cus_name_list = getCusNameList()
        # 返回用户列表
        qw.send_text("\n".join(cus_name_list), [admin_id])
    else:
        reply = getIdType(msg)
        try:
            result = json.loads(reply)
            tasks_id = result.get('tasks_id')
            category = result.get('category')
            names = getName(msg)
            logger.debug(f"解析消息结果: tasks_id={tasks_id}, category={category}, names={names}")
            # print(tasks_id)
            # print(cateogry)
            # tasks_id = list(map(str, tasks_id))
            # print(type(tasks_id))
            # print(cateogry)
            # 已审批的信息查询不到
            # 取到topk个任务的信息
            # 查看待审批任务
            if category == "view":
                message = ""
                # 查看所有任务
                if not tasks_id or len(tasks_id) >= 10:
                    # 查看名下所有任务
                    if names:
                        dict = getReverseDict()
                        for name in names: 
                            task_list = getTaskIdsByUid(dict,name)
                            if len(task_list):
                                message += f"{name}名下共{len(task_list)}个任务：\n"
                                for i in range(0, len(task_list), 4):
                                    # 每四个task_id为一行输出
                                    format_line_tasks = task_list[i:i+4]
                                    message += " ".join(format_line_tasks) + "\n"
                            else:
                                message += f"{name}不在待审批用户列表中。\n"
                    else:
                        # 查看topk个任务
                        message += viewTopk(3) 
                # 查看具体id的任务
                else:
                    for id in tasks_id:
                        message += viewInfo(id)
                        message += "\n"
                qw.send_text(message, [admin_id])
            # 通过待审批任务
            elif category == "accept":
                # 提取出来的id为空：审批所有的
                if not tasks_id:
                    tasks_id = getTasksID()
                    # tasks_id = [key.decode("utf-8").split('_')[-1] for key in client.keys('waitt_*')]
                cus_status = pendApprovalList(tasks_id, admin_id, True)
                # print(cus_status)
                printAprroval(cus_status)
                logger.info(f"管理员 {admin_id} 批准通过任务: {tasks_id}")
            # 不通过待审批任务
            elif category == "reject":
                if not tasks_id:
                    tasks_id = getTasksID()
                    # tasks_id = [key.decode("utf-8").split('_')[-1] for key in client.keys('waitt_*')]
                cus_status = pendApprovalList(tasks_id, admin_id, False)
                # print(cus_status)
                printAprroval(cus_status)
                logger.info(f"管理员 {admin_id} 拒绝任务: {tasks_id}")
            # elif category == "check":

            else:
                qw.send_text("请输入具体的操作和任务ID。\n", [admin_id])
                logger.warning(f"管理员 {admin_id} 输入了无效的操作和任务ID。") 
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            qw.send_text(reply, [admin_id])            
time.sleep(2)

