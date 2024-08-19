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
        return "检测通过，已通知管理员进行审批。"
    
    issues = [item for item in msg if item is not None]
    output = f"任务{task_id}存在以下问题：\n"
    for index, issue in enumerate(issues, start=1):
        output += f"{index}. {issue}\n"
    
    logger.warning(f"Task {task_id} has issues: {issues}")
    return output.strip()

def checkId(tasks_id: list) -> list:
    combined_msgs = []
    for id in tasks_id:
        logger.debug(f"Checking ID: {id}")
        return_info = combine(id)
        judge_id = return_info.taskId
        try:
            if not judge_id:
                raise ValueError("Data is empty")
            msg_list = checkRules(return_info)
        except ValueError as e:
            logger.error(f"ValueError for task ID {id}: {e}")
            msg_list = ["没有查询到相关的任务，请检查输入的任务ID是否正确"]
        return_msg = returnMsg(id, msg_list)
        combined_msgs.append(return_msg)
    return combined_msgs

def getData(k: bytes) -> str:
    k = k.decode("utf-8")
    logger.debug(f"Processing key: {k}")
    if k.startswith("msg_"):
        msg = r.lpop(k)
        msg = msg.decode("utf-8")
        logger.info(f"User {k} said: {msg}")
    return get_answer(msg)

while True:
    keys = r.keys()
    for k in keys:
        data = getData(k)
        try:
            answer = json.loads(data)
            if isinstance(answer, dict):
                tasks_id = answer.get('tasks_id')
                combined_msgs = checkId(tasks_id)
                qw.send_text("\n\n".join(combined_msgs) + "\n\n请解决以上的问题。", ["17a755177f4ad1f1d99bf8042cfbb74a"])
        except json.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}")
            qw.send_text(data, ["17a755177f4ad1f1d99bf8042cfbb74a"])
        except PermissionError as e:
            logger.error(f"PermissionError: {e}")
            qw.send_text("用户没有权限，请联系管理员进行处理。", ["17a755177f4ad1f1d99bf8042cfbb74a"])
        except MemoryError as e:
            logger.critical(f"MemoryError: {e}")
            qw.send_text("发生了内存错误，请联系管理员进行处理。", ["17a755177f4ad1f1d99bf8042cfbb74a"])
        except SystemExit as e:
            logger.critical(f"SystemExit: {e}")
            qw.send_text("发生了系统退出，请联系管理员进行处理。", ["17a755177f4ad1f1d99bf8042cfbb74a"])
        except KeyboardInterrupt as e:
            logger.critical(f"KeyboardInterrupt: {e}")
            qw.send_text("发生了键盘中断，请联系管理员进行处理。", ["17a755177f4ad1f1d99bf8042cfbb74a"])
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            qw.send_text("系统出现异常，请联系管理员进行处理。", ["17a755177f4ad1f1d99bf8042cfbb74a"])
    time.sleep(2)
