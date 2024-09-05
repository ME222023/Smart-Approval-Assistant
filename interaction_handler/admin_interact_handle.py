import re
import time
import json
import logging
from typing import List

from LLM.assistant import get_tasks_id_category, get_names
from scheduler.schedule_handle import get_latest_task_info, approval, get_task_list_by_user, get_applicant_id
from redis_handler.redis_handle import RedisClient
from utils.config import Config
from rule_handler.rules import check_rules
from redis_handler.redis_task_utils import get_cus_name_list, get_taskid_cusid_dict, get_cusid_taskid_dict, get_taskid_list

logger = logging.getLogger("server_log")

def update_task_status_dict(task_dict: dict, user_name: str, status: str, admin_id: str) -> dict:
    """
    "通过"或者"不通过"任务的状态更新
    @param task_dict: (cus_id,task_id)字典
    @param user_name: 要查看的用户名称
    @param status: "通过"或"不通过"的状态
    @param admin_id: 执行操作的管理员ID
    @return: 返回更新任务状态之后的(task_id,stastus)字典
    """
    # 初始化一个新的字典用于存储更新后的任务状态
    updated_dict = {}
    combine_str = ""
    # 获取所有键
    uid_list = list(task_dict.keys())
    user_id = Config.get_uid_uname(None,user_name)
    if not user_id:
        Config.wechat_client.send_text("没有查询到用户名，请确保用户名输入正确。", [admin_id])
        return {}
    if user_id in uid_list:
        # 遍历输入字典
        for uid, tasks in task_dict.items():
            # 如果当前用户ID匹配需要更新的用户ID
            if uid == user_id:
                # 将任务列表转换为任务状态字典
                updated_dict[uid] = {task_id: status for task_id in tasks}
                for task_id in tasks:
                    combine_str += f"已完成任务{task_id}的审批。\n"
                    if status == "通过":
                        approval(task_id, True)
                    elif status == "不通过":
                        approval(task_id, False)
                    with RedisClient(Config.redis_url) as client:   
                        client.delete(f"waitt_{task_id}")
            else:
                # 其他用户的任务保持不变
                updated_dict[uid] = {task_id: "未处理" for task_id in tasks}
        Config.wechat_client.send_text(combine_str, [Config.admin_ids])
        return updated_dict
    else:
        Config.wechat_client.send_text(f"已经处理完成{user_name}名下所有任务或{user_name}名下不存在待审批任务。", [admin_id])
        return {}
    

def view_info(task_id: str) -> str:
    """
    输入"查看"且有任务ID：
    若为待审批任务，则返回部分调度信息
    @param task_id: 查看的调度任务ID
    @return: 返回部分调度信息
    """
    logger.debug(f"检查任务信息，任务ID: {task_id}")
    message = ""
    try:
        info = get_latest_task_info(task_id)
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

def view_topk_info(k: int = 3) -> str:
    """
    输入"查看"且没有任务ID：
    返回k个待审批任务的部分调度信息，k默认值为3
    @param k: 默认返回待审批任务的数量
    @return: 返回部分调度信息
    """
    logger.debug(f"检查前 {k} 个待审批任务信息")
    output = ""
    try:
        tasks_id = get_taskid_list()
        logger.debug(f"tasks_id={tasks_id}")
        # 取前 k 个 tasks_id
        top_k_tasks_id = tasks_id[:k]
        # 列表中实际有的任务
        length = len(top_k_tasks_id)
        if not tasks_id:
            output += "待审批任务列表为空，暂时没有可以查看详情的任务。"
            logger.info("目前没有待审批的任务。")
        else:
            for task_id in top_k_tasks_id:
                output += view_info(task_id)
                output += "\n\n"
            output += f"以上只显示了待审批队列中前{length}个任务的信息。"
            logger.info(f"显示了待审批队列中前 {length} 个任务的信息。")
    except Exception as e:
        logger.error(f"检查待审批任务信息失败，错误: {e}")
        output += "检查待审批任务信息时发生错误，请确保输入了正确的任务ID或用户名。"
    return output      

     
def approve_pending_tasks(tasks_id: List[str], admin_id: str, wait_approve = True) -> dict:
    """
    得到的字典结构:
    {adminA_id: [{task1_id: "通过", task2_id: "不通过"}], adminB_id: [{task3_id: "通过"}]}
    @param tasks_id: 管理员请求中提取的任务ID列表
    @param admin_id: 管理员ID
    @param wait_approve: 待审批任务通过与否的判断，默认为True即通过，False即不通过
    @return: 返回待审批任务和是否通过的字典
    """
    logger.debug(f"管理员 {admin_id} 请求审批任务: {tasks_id}, 审批状态: {'通过' if wait_approve else '不通过'}")
    wait_tasks = get_taskid_list()
    if not wait_tasks:
        logger.info(f"待审批任务列表为空，管理员 {admin_id} 无任务可审批。")
        Config.wechat_client.send_text("待审批任务列表为空，暂时没有可以审批的任务。\n", [admin_id])
        return {}
    status = {}
    temp = {}
    combine_str = ""
    for t_id in tasks_id:
        if t_id not in wait_tasks:
            # 发送消息给admin：该任务id不存在
            logger.warning(f"任务 {t_id} 不存在，管理员 {admin_id} 输入错误。")
            Config.wechat_client.send_text(f"任务{t_id}不存在，请查看ID输入是否正确。\n", [admin_id])
            return {}
        else:
            # 获取与 task_id 关联的所有 cus_id
            with RedisClient(Config.redis_url) as client:   
                cus_ids = client.lrange(f"waitt_{t_id}", 0, -1)
            # 将字节类型转换为字符串
            cus_ids = [cus_id.decode('utf-8') for cus_id in cus_ids]
            logger.debug(f"任务 {t_id} 关联的用户ID: {cus_ids}")
            # approval操作是否成功
            msg = ""
            if wait_approve:
                status[t_id] = "通过"
                msg = approval(t_id)  # 通过：True
                with RedisClient(Config.redis_url) as client:   
                    client.delete(f"waitt_{t_id}")
                logger.info(f"任务 {t_id} 已审批通过。")
            # 批准不通过
            else:
                status[t_id] = "不通过"
                msg = approval(t_id, False)  # 不通过：False
                logger.info(f"任务 {t_id} 审批不通过。")
            if msg == "操作成功！":
                with RedisClient(Config.redis_url) as client:   
                    client.delete(f"waitt_{t_id}")
                combine_str += f"已完成任务{t_id}的审批。\n"
            else:
                combine_str += f"任务{t_id}审批操作异常，请管理员跟进处理。\n"
            # 更新 cus_status 字典
            for cus_id in cus_ids:
                if cus_id not in temp:
                    temp[cus_id] = {t_id: status[t_id]}
                else:
                    temp[cus_id][t_id] = status[t_id]
    Config.wechat_client.send_text(combine_str, [Config.admin_ids])
    return temp

def print_task_status(task_status: dict):
    """
    根据以下字典结构中任务通过与否的结果，回复对应的用户
    {adminA_id: [{task1_id: "通过", task2_id: "不通过"}], adminB_id: [{task3_id: "通过"}]}
    @param task_status: approve_pending_tasks函数得到的任务状态字典
    """
    logger.debug(f"生成输出，用户任务状态: {task_status}")
    for cus_id, tasks in task_status.items():
        messages = []
        for task_id, state in tasks.items():
            if state == "通过":
                messages.append(f"任务{task_id}已审批通过，请注意查看。\n")
                print(messages)
            elif state == "不通过":
                messages.append(f"任务{task_id}审批不通过，请修改后再做尝试。\n")
        # 消息不为空且cus_id不是管理员的  
        if messages and (cus_id not in Config.admin_ids):
            Config.wechat_client.send_text("\n".join(messages), [cus_id])

def get_tasks_by_unames(names: List[str]) -> str:
    """
    查看名下的所有任务ID列表:
    @param names: 要查看的名称列表
    @return: 返回名称列表的任务ID列表合并字符串
    """
    message = ""
    for name in names: 
        task_list = get_task_list_by_user(name)
        logger.debug(task_list)
        if len(task_list):
            message += f"{name}名下共{len(task_list)}个任务：\n"
            for i in range(0, len(task_list), 4):
                # 每四个task_id为一行输出
                format_line_tasks = task_list[i:i+4]
                message += " ".join(format_line_tasks) + "\n"
        else:
            message += f"{name}不在待审批用户列表中。\n"
    return message

def notify_admin_of_task_issues(task_id: str, msg_list: List[str], cus_id) -> str:
    """
    查看名下的所有任务ID列表:
    @param task_id: 要查看的名称列表
    @param msg_list: 规则检测后的消息提示列表
    @param cus_id: 任务对应的用户ID
    @return: 根据消息提示列表返回提示信息给管理员
    """
    msg = ""
    if all(item is None for item in msg_list):
        msg += f"任务{task_id}通过规则检测。"
        with RedisClient(Config.redis_url) as client: 
            logger.debug(cus_id)
            client.rpush(f"waitt_{task_id}", cus_id)
        return msg
    issues = [item for item in msg_list if item is not None]
    output = f"任务{task_id}存在的以下问题：\n"
    for index, issue in enumerate(issues, start=1):
        output += f"{index}. {issue}\n"
    output += "\n 请解决以上问题后再做尝试。\n"
    logger.warning(f"Task {task_id} has issues: {issues}")
    return output.strip()
    
def admin_interact(admin_id: str, msg: str):
    """
    查看名下的所有任务ID列表:
    @param admin_id: 交互的管理员ID
    @param msg: 管理员收到的信息
    @return: 管理员和小智的交互
    """
    logger.debug(f"管理员 {admin_id} 收到消息: {msg}")
    pattern = r"查看待审批用户"
    if re.search(pattern, msg):
        cus_name_list = get_cus_name_list()
        # 返回用户列表
        if cus_name_list:
            Config.wechat_client.send_text("\n".join(cus_name_list), [admin_id])
        else:
            Config.wechat_client.send_text("待审批队列中没有待审批的调度信息。", [admin_id])
    else:
        reply = get_tasks_id_category(msg)
        try:
            result = json.loads(reply)
            tasks_id = result.get('tasks_id')
            category = result.get('category')
            names = get_names(msg)
            logger.debug(f"解析消息结果: tasks_id={tasks_id}, category={category}, names={names}")
            # 取到topk个任务的信息
            # 查看待审批任务
            dict = get_cusid_taskid_dict()                                                                                            
            logger.debug(dict)
            if category == "view":
                message = ""
                # 查看所有任务
                if not tasks_id or len(tasks_id) >= 10:
                    # 查看名下所有任务
                    if names:
                        message += get_tasks_by_unames(names)
                    else:
                        message += view_topk_info(3) 
                # 查看具体id的任务
                else:
                    for t_id in tasks_id:
                        message += view_info(t_id)
                        message += "\n"
                Config.wechat_client.send_text(message, [admin_id])
            # 通过待审批任务
            elif category == "accept":
                # 提取出来的id为空：审批所有的
                cus_status = {}
                if not tasks_id:
                    for name in names:
                        cus_status = update_task_status_dict(dict,name,"通过",admin_id)
                else:
                    cus_status = approve_pending_tasks(tasks_id, admin_id, True)
                if cus_status:
                    logger.debug(cus_status)
                    print_task_status(cus_status)
                    logger.info(f"管理员 {admin_id} 批准通过任务: {tasks_id}")
                else:
                    Config.wechat_client.send_text("请输入正确的ID或用户名。", [admin_id])
            # 不通过待审批任务
            elif category == "reject":
                cus_status = {}
                if not tasks_id:
                    for name in names:
                        cus_status = update_task_status_dict(dict,name,"不通过",admin_id)
                else:
                    cus_status = approve_pending_tasks(tasks_id, admin_id, False)
                if cus_status:
                    logger.debug(cus_status)
                    print_task_status(cus_status)
                    logger.info(f"管理员 {admin_id} 拒绝任务: {tasks_id}")
                else:
                    Config.wechat_client.send_text("请输入正确的ID或用户名。", [admin_id])
            elif category == "check":
                if not tasks_id:
                    Config.wechat_client.send_text("请输入需要检查的任务ID。", [admin_id])
                else:
                    # 待审批队列当中的id
                    combined_msgs = []
                    for t_id in tasks_id:
                        # 待审批队列id列表
                        task_list = get_taskid_list()
                        logger.debug(f"waitt_task_list: {task_list}")
                        # 若t_id在待审批队列当中
                        if t_id in task_list:
                            logger.debug(f"t_id: {t_id}")
                            task_user_id_dict = get_taskid_cusid_dict()
                            logger.debug(task_user_id_dict)
                            cus_id = task_user_id_dict[t_id]
                            if not cus_id:
                                cus_id = get_applicant_id(t_id)
                        else:
                            # cus_id为空的话，以(waitt_{task_id},applicant_id)入队列
                            cus_id = get_applicant_id(t_id)
                            logger.debug(f"cus_id: {cus_id}")
                        return_info = get_latest_task_info(t_id)
                        logger.debug(f"return_info: {return_info}")
                        judge_id = return_info.taskId
                        if not judge_id:
                            logger.error(f"ValueError for task ID {t_id}")
                            msg_list = ["没有查询到相关的任务。\n请检查输入的任务ID是否正确。"]
                        else:
                            msg_list = check_rules(return_info, cus_id)
                        logger.debug(f"msg_list: {msg_list}")
                        if cus_id:
                            return_msg = notify_admin_of_task_issues(t_id, msg_list, cus_id)
                            logger.debug(return_msg)
                            if return_msg:
                                combined_msgs.append(return_msg)
                            logger.debug(combined_msgs)
                        else:
                            combined_msgs.append(f"查询不到{t_id}任务调度信息的申请人。")
                    Config.wechat_client.send_text("\n\n".join(combined_msgs), [admin_id])
            else:
                Config.wechat_client.send_text("请输入具体的操作和任务ID。\n", [admin_id])
                logger.warning(f"管理员 {admin_id} 输入了无效的操作和任务ID。") 
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            Config.wechat_client.send_text(reply, [admin_id])            
time.sleep(1)