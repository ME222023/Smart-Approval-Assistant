import time
import json
import logging
from typing import List, Optional


from LLM.assistant import get_answer
from scheduler.schedule_handle import get_latest_task_info
from rule_handler.rules import check_rules
from redis_handler.redis_handle import RedisClient
from utils.exception_handle import LoginException, CheckException
from utils.config import Config

logger = logging.getLogger("server_log")

def send_admin_msg(task_id: str, msg: List[str]) -> str:
    """
    生成请求审批后管理员的返回信息
    @param task_id: 用户申请的任务ID
    @param msg: 规则匹配后的消息队列
    @return: 用户的返回信息
    """
    with RedisClient(Config.redis_url) as client:   
        wait_tasks = [key.decode("utf-8").split('_')[-1] for key in client.keys('waitt_*')]
    output = ""
    if all(item is None for item in msg) and task_id not in wait_tasks:
        output += f"任务{task_id}已通过规则检测，请进行审批。"
    return output


def send_cus_msg(task_id: str, error_list: List[str], cus_id: str) -> str:
    """
    生成用户的返回信息
    @param task_id: 用户申请的任务ID
    @param msg: 规则匹配后的消息队列
    @return: 用户的返回信息
    """
    logger.debug(f"Processing task_id: {task_id} with messages: {error_list}")
    with RedisClient(Config.redis_url) as client:   
        wait_tasks = [key.decode("utf-8").split('_')[-1] for key in client.keys('waitt_*')]
    # 函数返回给用户的信息
    msg = ""
    if task_id in wait_tasks:
        msg += f"任务{task_id}已经通知管理员进行审批，无需重复申请。"
        return msg
    else:
        # 规则检测没有任何问题
        if all(item is None for item in error_list):
            msg += f"任务{task_id}通过规则检测，已通知管理员进行审批。"
            logger.info(f"Task {task_id} passed the check.")
            # 通过规则审批，任务加入待审批队列
            with RedisClient(Config.redis_url) as client: 
                client.rpush(f"waitt_{task_id}", cus_id)
            return msg
        
        # 规则检测存在问题
        issues = [item for item in error_list if item is not None]
        output = f"任务{task_id}存在的以下问题：\n"
        for index, issue in enumerate(issues, start=1):
            output += f"{index}. {issue}\n"
        logger.warning(f"Task {task_id} has issues: {issues}")
        return output.strip()


def check_task_id(tasks_id: List[str], cus_id: str) -> [List[str], Optional[None]]:
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
    else:
        for t_id in tasks_id:
            logger.debug(f"Checking ID: {t_id}")
            return_info = get_latest_task_info(t_id)
            logger.debug(f"Task info combine: {return_info}")
            judge_id = return_info.taskId
            if not judge_id:
                logger.error(f"ValueError for task ID {t_id}")
                msg_list = ["没有查询到相关的任务。\n请检查输入的任务ID是否正确。"]
            else:
                msg_list = check_rules(return_info, cus_id)
                logger.debug(f"------------msg_list={msg_list}")
            return_msg_ad = send_admin_msg(t_id, msg_list)
            return_msg_cus = send_cus_msg(t_id, msg_list, cus_id)
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
  
def get_LLM_answer(k: bytes) -> str:
    """
    消息存储的键值对(msg_{ID},message)
    根据msg_{ID}得到LLM回复的字符串
    @param k: 申请者的msg_{ID}键值
    @return: 返回LLM回复的字符串。
    """
    logger.debug(f"Processing key: {k}")
    with RedisClient(Config.redis_url) as client: 
        msg = client.lpop(k)
    msg = msg.decode("utf-8")
    logger.info(f"User {k} said: {msg}")
    res_msg = get_answer(msg)
    logger.info("-------> getData: {}".format(res_msg))
    return res_msg

def cus_interact(k: str, cus_id: str):
    """
    与用户申请者的交互
    @param k: 用户申请者的msg_{ID}键值
    @param cus_id: 用户申请者ID
    """
    answer = get_LLM_answer(k)
    try:
        result = json.loads(answer)
        tasks_id = result.get('tasks_id')
        logger.debug(f"tasks_id:{tasks_id}")
        combined_msgs, combined_ad = check_task_id(tasks_id, cus_id)
        logger.debug(f"combined_msgs: {combined_msgs}, combined_ad: {combined_ad}")
        if combined_ad:
            # 发送合并后的消息给管理员
            Config.wechat_client.send_text(combined_ad, [Config.admin_ids])
        Config.wechat_client.send_text("\n\n".join(combined_msgs), [cus_id])  
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        Config.wechat_client.send_text(answer, [cus_id])
    except PermissionError as e:
        logger.error(f"PermissionError: {e}")
        Config.wechat_client.send_text("没有权限，已通知管理员进行处理。", [cus_id])
        Config.wechat_client.send_text(f"用户{cus_id}没有权限，请管理员进行处理。", [Config.admin_ids])
    except MemoryError as e:
        logger.error(f"MemoryError: {e}")
        Config.wechat_client.send_text("发生了内存错误，已通知管理员进行处理。", [cus_id])
        Config.wechat_client.send_text("发生了内存错误，请管理员进行处理。", [Config.admin_ids])
    except SystemExit as e:
        logger.error(f"SystemExit: {e}")
        Config.wechat_client.send_text("发生了系统退出，已通知管理员进行处理。", [cus_id])
        Config.wechat_client.send_text("发生了系统退出，请管理员进行处理。", [Config.admin_ids])
    except LoginException as e:
        logger.error(f"LoginException: {e}")
        Config.wechat_client.send_text("登录失败，请重新登录授权。", [Config.admin_ids])
        Config.wechat_client.send_text("登录失败，已通知管理员进行处理。", [cus_id])
    except CheckException as e:
        logger.error(f"CheckException: {e}")
        Config.wechat_client.send_text("任务查找失败，请输入正确的ID。", [cus_id])
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        Config.wechat_client.send_text("系统出现异常，已通知管理员进行处理。", [cus_id])
        Config.wechat_client.send_text("系统出现异常，请管理员进行处理。", [Config.admin_ids])
time.sleep(2)

