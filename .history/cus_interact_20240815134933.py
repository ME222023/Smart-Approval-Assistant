import redis
import time
import json
import logging
from typing import Union, List, Optional
from LLM.assistant import get_answer
from chat.send_app import qywx
from scheduler.schedule_handle import *
from ruler_handle.rules import *
from utils.redis_handle import RedisClient

from utils.exception_handle import LoginException


# from trial import checkInfo

# redis_url = "redis://:123@10.5.5.73:16379/v1"
# redis_url = "redis://:123@10.5.5.73:16379/1"
# r = redis.from_url(redis_url)

# 管理员的id
admin_ids = [
    "17a755177f4ad1f1d99bf8042cfbb74a",
    "1730846d950e0a5709ac2ea44138df09"
]

qw = qywx()

# 创建一个日志记录器
logger = logging.getLogger("server_log")


# def checkId(tasks_id: list, cus_id: str) -> list:
def adminMsg(task_id: str = None, msg: list = None) -> str:
    # print(task_id)
    """
    生成请求审批后管理员的返回信息
    @param task_id: 用户申请的任务ID
    @param msg: 规则匹配后的消息队列
    @return: 用户的返回信息
    """
    with RedisClient(redis_url="redis://:123@10.5.5.73:16379/v1") as client:   
        wait_tasks = [key.decode("utf-8").split('_')[-1] for key in client.keys('waitt_*')]
    # print(wait_tasks)
    # print(task_id, type(task_id))
    # print(task_id in wait_tasks)
    # print(task_id not in wait_tasks)
    output = ""
    if all(item is None for item in msg) and task_id not in wait_tasks:
        output += f"任务{task_id}已通过规则检测，请进行审批。"
    return output


def cusMsg(task_id: str = None, msg: list = None, cus_id: str = None) -> str:
    """
    生成管理员的返回信息
    @param task_id: 用户申请的任务ID
    @param msg: 规则匹配后的消息队列
    @return: 用户的返回信息
    """
    logger.debug(f"Processing task_id: {task_id} with messages: {msg}")
    with RedisClient(redis_url="redis://:123@10.5.5.73:16379/v1") as client:   
        wait_tasks = [key.decode("utf-8").split('_')[-1] for key in client.keys('waitt_*')]
    if all(item is None for item in msg):
        # 入待审批队列
        # print("--------------------------------------------------------")
        msg = ""
        if task_id in wait_tasks:
            msg += f"任务{task_id}已经通知管理员进行审批，无需重复申请。"
        else:
            msg += f"任务{task_id}通过规则检测，已通知管理员进行审批。"
            logger.info(f"Task {task_id} passed the check.")
            # 通过规则审批，任务加入待审批队列
            with RedisClient(redis_url="redis://:123@10.5.5.73:16379/v1") as client: 
                client.rpush(f"waitt_{task_id}", cus_id)
        # print(type(task_id))
        # ktest = r.keys()
        # for k in ktest:
        #     print(type(k))
        # print("--------------------------------------------------------")
        # msg = wait_approval.lpop(f"msg_{cus_id}")
        # print(msg)
        return msg
    
    issues = [item for item in msg if item is not None]
    output = f"任务{task_id}存在的以下问题：\n"
    for index, issue in enumerate(issues, start=1):
        output += f"{index}. {issue}\n"
    # output += "\n 请解决以上问题后再做尝试。\n"
    logger.warning(f"Task {task_id} has issues: {issues}")
    return output.strip()


def checkId(tasks_id: list, cus_id: str) -> [List[str], Optional[None]]:
    """
    返回规则检测后回复用户的字符串
    根据msg_{ID}得到LLM回复的字符串
    @param tasks_id: LLM根据用户请求提取的任务ID列表
    @param cus_id: 用户ID
    @return: 返回回复用户的字符串
    """
    combined_msgs = []
    combined_ad = []
    if not tasks_id:
        msg_list = ["没有提取到任务ID。\n请检查是否输入了任务ID。"]
        return msg_list, None
        # combined_msgs.append("没有提取到任务ID。\n请检查是否输入了任务ID。")
    else:
        for id in tasks_id:
            logger.debug(f"Checking ID: {id}")
            return_info = getLatestTaskInfo(id)
            logger.debug(f"Task info combine: {getLatestTaskInfo}")
            judge_id = return_info.taskId
            if not judge_id:
                logger.error(f"ValueError for task ID {id}")
                msg_list = ["没有查询到相关的任务。\n请检查输入的任务ID是否正确。"]
            else:
                msg_list = checkRules(return_info, cus_id)
            return_msg_ad = adminMsg(id, msg_list)
            return_msg_cus = cusMsg(id, msg_list, cus_id)
            if return_msg_cus:
                combined_msgs.append(return_msg_cus)
                print(combined_msgs)
            if return_msg_ad:
                combined_ad.append(return_msg_ad)
                print(combined_ad)
    combined_msgs.append("请解决以上存在的问题后再做尝试。\n")

    logger.debug(f"combined_ad: {combined_ad}, combined_msgs: {combined_msgs}")
    if combined_ad:
        return combined_msgs, "\n\n".join(combined_ad)
    else:
        return combined_msgs, None

  
    def getData(k: bytes) -> str:
        """
        消息存储的键值对(msg_{ID},message)
        根据msg_{ID}得到LLM回复的字符串
        @param k: 申请者的msg_{ID}键值
        @return: 返回LLM回复的字符串。
        """
        logger.debug(f"Processing key: {k}")
        with RedisClient(redis_url="redis://:123@10.5.5.73:16379/v1") as client: 
            msg = client.lpop(k)
        msg = msg.decode("utf-8")
        logger.info(f"User {k} said: {msg}")
        res_msg = get_answer(msg)
        logger.info("-------> getData: {}".format(res_msg))
        return res_msg

# 输入：需要查看的任务id列表
# def getInfo(tasks_id: list):
#     tasks_id = result.get('tasks_id')
#     for id in tasks_id:
#         checkInfo(id)

# 输入：已审批列表中的所有id
# 通过所有的id
# def okAll(tasks_id: list):
#    for id in tasks_id:
#        approval(id)


# def okPart(tasks_id: list):
#     for id in tasks_id:
#         approval(id,False)

# "通过批准" in msg: 传入wait_approval的所有task_id组成的tasks_id:list和True
# "通过" 123 in msg: 传入wait_approval中指定的task_id组成的tasks_id:list和True
# "不通过批准" in msg: none和False，wait_approval的所有task_id lpop
# "不通过" 123 in msg: 123和False，lpop同时wait_approval中除123以外的所有id都"通过批准"


# def admApproval(tasks_id: list, approval =  True):
#     for id in tasks_id:
#         if id not in wait_tasks:
            



# def checkMsg(msg:list) -> list:
#     if "问题" in msg[0]:

# 别名测试：
# data = {
#     'apple': 'SELECT * FROM table_name;',
#     'apple2': 'INSERT INTO table_name (column1, column2) VALUES (value1, value2);',
#     'apple3': 'source_db'
# }

# model = scheduleInfo(**data)
# print(model.select_sql)  # 输出: SELECT * FROM table_name;
# print(model.insert_sql)  # 输出: INSERT INTO table_name (column1, column2) VALUES (value1, value2);
# print(model.source_database_name)  # 输出: source_db
# print(model.dict(by_alias=True))  
# 输出: {'select.sql': 'SELECT * FROM table_name;', 'insert.sql': 'INSERT INTO table_name (column1, column2) VALUES (value1, value2);', 'source.database.name': 'source_db'}

# def ():
#     with RedisClient(redis_url="redis://:123@10.5.5.73:16379/v1") as client:
#         while True:
#             keys = client.keys()
#             for k in keys:
#                 k = k.decode("utf-8")
#                 if not k.startswith("msg_"):
#                     continue
#                 # 用户的id信息
#                 from_id = k.split("_")[-1]
#                 cus_id = f"{from_id}"
#                 answer = getData(k)
#                 # print(answer)
#                 # print(cus_id)
#                 try:
#                     result = json.loads(answer)
#                     tasks_id = result.get('tasks_id')
#                     # print(type(tasks_id))
#                     # print(tasks_id)
#                     combined_msgs = checkId(tasks_id, cus_id)
#                     # print(combined_msgs)
#                     # print("------------------------------------------------")
#                     # id_list = getWait()
#                     # print(id_list)
#                     # print(combined_msgs)
#                     # 请帮我审批10038968和10038968两个任务
#                     # if "问题" in combined_msgs:
#                     # f"{from_id}"
#                     qw.send_text("\n\n".join(combined_msgs), [cus_id])  
#                 except json.JSONDecodeError as e:
#                     logger.error(f"JSON decode error: {e}")
#                     qw.send_text(answer, [cus_id])
#                 except PermissionError as e:
#                     logger.error(f"PermissionError: {e}")
#                     qw.send_text("没有权限，已通知管理员进行处理。", [cus_id])
#                     qw.send_text(f"用户{cus_id}没有权限，请管理员进行处理。", [admin])
#                 except MemoryError as e:
#                     logger.critical(f"MemoryError: {e}")
#                     qw.send_text("发生了内存错误，已通知管理员进行处理。", [cus_id])
#                     qw.send_text("发生了内存错误，请管理员进行处理。", [admin])
#                 except SystemExit as e:
#                     logger.critical(f"SystemExit: {e}")
#                     qw.send_text("发生了系统退出，已通知管理员进行处理。", [cus_id])
#                     qw.send_text("发生了系统退出，请管理员进行处理。", [admin])
#                 except Exception as e:
#                     logger.critical(f"Unexpected error: {e}")
#                     qw.send_text("系统出现异常，已通知管理员进行处理。", [cus_id])
#                     qw.send_text("系统出现异常，请管理员进行处理。", [admin])
#             time.sleep(2)
# with RedisClient(redis_url="redis://:123@10.5.5.73:16379/v1") as client:
    # client.flushdb()

def cusInteract(k: str, cus_id: str):
    """
    与用户申请者的交互
    @param k: 用户申请者的msg_{ID}键值
    @param cus_id: 用户申请者ID
    """
    answer = getData(k)
    try:
        result = json.loads(answer)
        tasks_id = result.get('tasks_id')
        print(tasks_id)
        # combined_msgs = checkId(tasks_id, cus_id)
        logger.debug("---------------")
        combined_msgs, combined_ad = checkId(tasks_id, cus_id)
        logger.debug(f"combined_msgs: {combined_msgs}, combined_ad: {combined_ad}")
        if combined_ad:
            # 发送合并后的消息给管理员
            qw.send_text("\n\n".join(combined_ad), admin_ids)
        qw.send_text("\n\n".join(combined_msgs), [cus_id])  
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        qw.send_text(answer, [cus_id])
    except PermissionError as e:
        logger.error(f"PermissionError: {e}")
        qw.send_text("没有权限，已通知管理员进行处理。", [cus_id])
        qw.send_text(f"用户{cus_id}没有权限，请管理员进行处理。", admin_ids)
    except MemoryError as e:
        logger.error(f"MemoryError: {e}")
        qw.send_text("发生了内存错误，已通知管理员进行处理。", [cus_id])
        qw.send_text("发生了内存错误，请管理员进行处理。", admin_ids)
    except SystemExit as e:
        logger.error(f"SystemExit: {e}")
        qw.send_text("发生了系统退出，已通知管理员进行处理。", [cus_id])
        qw.send_text("发生了系统退出，请管理员进行处理。", admin_ids)
    except LoginException as e:
        logger.error(f"LoginException: {e}")
        qw.send_text("登录失败，请重新授权！！！", admin_ids)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        qw.send_text("系统出现异常，已通知管理员进行处理。", [cus_id])
        qw.send_text("系统出现异常，请管理员进行处理。", admin_ids)
time.sleep(2)

# combined_msgs = checkId([10038971], "17a755177f4ad1f1d99bf8042cfbb74a")
# print(combined_msgs)
# qw.send_text("\n\n".join(combined_msgs), "17a755177f4ad1f1d99bf8042cfbb74a")  

