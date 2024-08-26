import time
import json
import logging
import requests
from typing import List

 
from utils.exception_handle import LoginException
from rule_handler.schema import ScheduleInfo
from utils.config import Config

logger = logging.getLogger("server_log")

api_key = "app-vdxlirpInaNyVZKhKSk99k3U"
large_model_url = 'http://10.5.5.73:10012/v1/chat-messages'

HEADERS = {
        "content-type": "application/json",
        "Authorization": f"Bearer {Config.token}",
        "Origin": Config.base_url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
}

def get_task_list(task_id: str = None, user: str = None):
    """
    根据给定的任务 ID 和用户名，获取待审批的任务列表。
    @param task_id: 任务 ID，用于筛选任务。
    @param user: 用户名，用于筛选申请人。
    @return: 返回包含任务记录的列表，如果操作失败则抛出 LoginException 异常。
    """
    url = f"{Config.base_url}/api/v1/task-approval/approval/waiting"

    query_str = {"page":"1","size":"500"}

    payload = {
        "applicant": user,
        "applicantTime": "",
        "createTime": "",
        "status": "",
        "taskName": "",
        "taskId": task_id,
        "taskType": "",
        "topicName": ""
    }

    response = requests.post(url, json=payload, headers=HEADERS, params=query_str)

    task_statu = response.json().get("message")

    if task_statu=="操作成功！":
        tasks = response.json().get("data").get("records")
        return tasks
    else:
        raise LoginException("登陆失败，请重新授权。")

def get_task_info(t_id: str) -> dict:
    """
    根据t_id获取任务的详细信息。
    @param t_id: 区别于task_id
    @return: 包含任务详细信息的字典，如果请求失败或任务不存在则返回空字典。
    """
    url = f"{Config.base_url}/api/v1/task-approval/approval/{t_id}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    if data.get("code") == 0:
        data = data.get("data")
        return {"data": data}
    return {}

def get_latest_task_info(task_id: str) -> ScheduleInfo:
    """
    返回提取信息后合并的调度信息
    @param task_id: 任务ID
    @return: 返回调度信息。
    """
    t_id = get_tid(task_id)
    info = get_task_info(t_id)
    data_task = info.get('data', {}).get('taskDtoLatest', {}).get('task', {})
    data_map = info.get('data', {}).get('taskDtoLatest', {}).get('map', {})
    data_merge = {**data_task, **data_map}
    json_str = json.dumps(data_merge, ensure_ascii=False, indent=4)
    json_obj = json.loads(json_str)
    info_instance = ScheduleInfo(**json_obj)
    return info_instance

# 通过True，不通过 False
def approval(task_id: str, approval = True) -> str:
    """
    审批是否通过返回的字符串
    @param task_id: 待审批任务ID
    @param approval: 待审批任务通过与否的判断，默认为True即通过，False即不通过
    @return: 返回回复的消息
    """
    t_id = get_tid(task_id)
    url = f"{Config.base_url}/api/v1/task-approval/approval/{t_id}"
    
    if approval:
        payload = {"approvalComment":"审批通过", "approvalResult":"APPROVAL_PASSED", "taskId": str(task_id)}
    else:
        payload = {"approvalComment":"审批不通过，请任务开发者跟进处理。","approvalResult":"APPROVAL_NOT_PASSED","taskId": str(task_id)}

    logger.debug(f"payload: {payload}")
    response = requests.post(url, json=payload, headers=HEADERS)
    logger.debug(f"response: {response.json()}")
    # 操作成功结果：{"code":0,"message":"操作成功！","data":1}

    return response.json().get("message")
    

def get_task_list_by_user(user: str) -> List[str]:
    """
    根据用户名获取用户相关的任务 ID 列表。
    @param user: 用户名，用于筛选任务列表。
    @return: 包含任务 ID 的字符串列表。如果用户没有相关任务或用户名为空，则返回空列表。
    """
    if user != "":
        tt = get_task_list(user=user)
        if len(tt) > 0:
            task_list = []
            for t in tt:
                task_id = t.get("taskId")
                # 保证task_id为字符串
                task_list.append(str(task_id))
            return task_list
        else:
            return []
    else:
        return []


def get_tid(task_id: str) -> str:
    """
    根据给定的task_id获取对应的t_id。
    @param task_id: 任务ID，用于筛选任务列表。
    @return: 返回t_id，如果没有找到对应的任务则返回 None。
    """
    tt = get_task_list(task_id=task_id)
    if len(tt) > 0:
        for t in tt:  
            t_id = t.get("id")
            return t_id
    else:
        return None

def get_applicant_id(task_id: str) -> str:
    """
    根据给定的任务ID获取任务申请者的ID。
    @param task_id: 任务ID，用于筛选任务列表。
    @return: 返回任务申请者的 ID。如果没有找到对应的任务或申请者，则返回空字符串。
    """
    tt = get_task_list(task_id=task_id)
    if len(tt) > 0:
        for t in tt:
            applicant = t.get("applicant")
            # 通过申请者的名字得到对应的Id
            applicant_id = Config.get_uid_uname(None, applicant)          
            return applicant_id
    else:
        return ""
