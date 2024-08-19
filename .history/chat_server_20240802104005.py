import redis
import time
import json
import logging
from LLM.assistant import get_answer
from chat.send_app import qywx
from scheduler.schedule_handle import *
from ruler_handle.rules import *

redis_url = "redis://:123@10.5.5.73:16379/v1"
r = redis.from_url(redis_url)

admin_ids = p[]

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

def returnMsg(task_id: str, msg: list) -> str:
    logger.debug(f"Processing task_id: {task_id} with messages: {msg}")
    if all(item is None for item in msg):
        logger.info(f"Task {task_id} passed the check.")
        # qw.send_text("规则检测通过，请及时审批", ["17a755177f4ad1f1d99bf8042cfbb74a"])
        return f"任务{task_id}通过规则检测，已通知管理员进行审批。\n"
    
    issues = [item for item in msg if item is not None]
    output = f"任务{task_id}存在以下问题：\n"
    for index, issue in enumerate(issues, start=1):
        output += f"{index}. {issue}\n"
    print(output)
    logger.warning(f"Task {task_id} has issues: {issues}")
    return output.strip()

def checkId(tasks_id: list) -> list:
    combined_msgs = []
    for id in tasks_id:
        logger.debug(f"Checking ID: {id}")
        return_info = combine(id)
        judge_id = return_info.taskId
        if not judge_id:
            logger.error(f"ValueError for task ID {id}")
            msg_list = ["没有查询到相关的任务，请检查输入的任务ID是否正确"]
        else:
            msg_list = checkRules(return_info)
        return_msg = returnMsg(id, msg_list)
        combined_msgs.append(return_msg)
        print(combined_msgs)
    return combined_msgs

def getData(k: bytes) -> json:

    logger.debug(f"Processing key: {k}")
    msg = r.lpop(k)
    msg = msg.decode("utf-8")
    logger.info(f"User {k} said: {msg}")
    res_msg = get_answer(msg)
    logger.info("-------> getData: {}".format(res_msg))
    res_msg = json.loads(res_msg)
    return res_msg


# def checkMsg(msg:list) -> list:
#     if "问题" in msg[0]:
    
while True:
    keys = r.keys()
    for k in keys:
        k = k.decode("utf-8")
        if not k.startswith("msg_"):
            continue
        answer = getData(k)
        try:
            if isinstance(answer, dict):
                tasks_id = answer.get('tasks_id')
                combined_msgs = checkId(tasks_id)
                print(combined_msgs)
                # 请帮我审批10038968和10038968两个任务
                # if "问题" in combined_msgs:
                qw.send_text("\n\n".join(combined_msgs) + "\n\n请解决以上的问题。", ["17a755177f4ad1f1d99bf8042cfbb74a"])
        except json.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}")
            qw.send_text(answer, ["1730846d950e0a5709ac2ea44138df09"])
        except PermissionError as e:
            logger.error(f"PermissionError: {e}")
            qw.send_text("用户没有权限，已通知管理员进行处理。", ["1730846d950e0a5709ac2ea44138df09"])
        except MemoryError as e:
            logger.critical(f"MemoryError: {e}")
            qw.send_text("发生了内存错误，已通知管理员进行处理。", ["1730846d950e0a5709ac2ea44138df09"])
        except SystemExit as e:
            logger.critical(f"SystemExit: {e}")
            qw.send_text("发生了系统退出，已通知管理员进行处理。", ["1730846d950e0a5709ac2ea44138df09"])
        except KeyboardInterrupt as e:
            logger.critical(f"KeyboardInterrupt: {e}")
            qw.send_text("发生了键盘中断，已通知管理员进行处理。", ["1730846d950e0a5709ac2ea44138df09"])
        except Exception as e:
            logger.critical(f"Unexpected error: {e}")
            qw.send_text("系统出现异常，已通知管理员进行处理。", ["1730846d950e0a5709ac2ea44138df09"])
    time.sleep(2)