import time
import requests
from typing import List
from datetime import datetime


base_url = "http://dispatcher.k8stest.axzq.com.cn"
# 认证token
TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ7XCJ1c2VySWRcIjpcIjIwM1wiLFwidXNlcm5hbWVcIjpcInpoYW5nemg0XCIsXCJuYW1lXCI6XCLlvKDkuonovolcIixcImJ6XCI6XCJOT1JNQUwsQURNSU5cIixcImFkbWluXCI6dHJ1ZSxcImVuYWJsZWRcIjp0cnVlLFwibm9ybVJvbGVJZFwiOlwiXCIsXCJhY2NvdW50Tm9uRXhwaXJlZFwiOnRydWUsXCJhY2NvdW50Tm9uTG9ja2VkXCI6dHJ1ZSxcImNyZWRlbnRpYWxzTm9uRXhwaXJlZFwiOnRydWV9IiwiaXNzIjoiemhhbmd6aDQiLCJpYXQiOjE3MjI5MjY3NTIsImV4cCI6MTcyMzAxMzE1Mn0.uKWC4U-6J77C9X_g0fCYu9xsIJf7tPa3asgC8mr-bksBmJvL_uKntd9iMSdL6YwSpcJV2u1DRwnzqWoJCxAifg"

#-----------------------------------------
api_key = "app-vdxlirpInaNyVZKhKSk99k3U"
large_model_url = 'http://10.5.5.73:10012/v1/chat-messages'

HEADERS = {
        "content-type": "application/json",
        "Authorization": f"Bearer {TOKEN}",
        "Origin": base_url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
}

def task_list(task_id:str="", user:str=""):
    url = f"{base_url}/api/v1/task-approval/approval/waiting"

    querystring = {"page":"1","size":"500"}

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

    response = requests.post(url, json=payload, headers=HEADERS, params=querystring)

    task_statu = response.json().get("message")

    if task_statu=="操作成功！":
        tasks = response.json().get("data").get("records")
        return tasks
    else:
        raise "登陆失败"

def task_info1(t_id: str) -> dict:
    url = f"{base_url}/api/v1/task-approval/approval/{t_id}"
    response = requests.get(url, headers=HEADERS)
    # print(url)
    # print(response)
    data = response.json()
    # print(data)
    if data.get("code") == 0:
        data = data.get("data")
        return {"data": data}
    return {}

# 通过tasks_name得到task_info
def task_info2(t_name: str) -> dict:
    url = f"{base_url}/api/v1/task-approval/approval/{t_name}"
    response = requests.get(url, headers=HEADERS)
    
    data = response.json()
    print(data)
    if data.get("code") == 0:
        data = data.get("data")
        return {"data": data}
    return {}

def approval(task_id:str, approval=True):
    t_id = by_task_id(task_id)
    url = f"{base_url}/api/v1/task-approval/approval/{t_id}"
    
    if approval:
        payload = {"approvalComment":"审批通过", "approvalResult":"APPROVAL_PASSED", "taskId": str(task_id)}
    else:
        payload = {"approvalComment":"审批不通过，任务开发者跟进处理！！！","approvalResult":"APPROVAL_NOT_PASSED","taskId": str(task_id)}
    
    # return payload.get("approvalComment")
    print(payload)
    response = requests.post(url, json=payload, headers=HEADERS)
    print(response.json())

    # 打印提取的值
    # print(approval_comment)
    # {"code":0,"message":"操作成功！","data":1}

    return response.json().get("message")
    

# 通过True，不通过 False

# {'id': 28723, 'taskId': 10969, 'applicant': 'zhangxs1', 'applicantTime': '', 'approval': '', 'approvalComment': '', 'approvalResult': '', 'approvalStatus': 'W', 'createTime': '2022-01-19', 'lastUpdate': '2022-01-19', 'taskType': 'Db2Hive', 'taskName': 'scgz_trakgdb_bj_bond', 'topicName': '实时资产数据采集'}

def by_user(user: str, approval = True):
    if user != "":
        print("通过开发者信息审批")
        tt = task_list(user=user)
        for t in tt:
            t_id = t.get("id")
            task_id = t.get("taskId")
            print(f'查询到任务task_id --> {task_id}, 任务开发者---> {t.get("applicant")}, 任务日期---> {t.get("createTime")}, , 任务主题---> {t.get("topicName")}')
            # message = approval(t_id, task_id, approval=approval)
            # if message == "操作成功！":
            #     print(f"task {task_id} 审批成功！")


# def by_task_id(task_ids: str, approval=True) -> str:
#     if len(task_ids) > 0:
#         print("通过task_id审批")
#         # t_id_list = []  # 用于存储 t_id 的列表
#         for task_id in task_ids:
#             tt = task_list(task_id=task_id)
#             # if len(tt) > 0:
#             for t in tt:
#                 # t = tt[0]
#                 t_id = t.get("id")
#                 return t_id
#                 # print(t_id)
#                 # t_id_list.append(t_id)
#                 # print(f'查询到任务task_id --> {task_id}, 任务开发者---> {t.get("applicant")}, 任务日期---> {t.get("createTime")}')
#                 # message = approval(task_id, approval=approval)
#                 # if message == "操作成功！":
#                 #     print(f"task {task_id} 审批成功！")
#     #     return t_id_list
#     # else:
#     #     print("没有提供task_id")
#     #     return []  # 如果 task_ids 为空，则返回空列表

def by_task_id(task_id: str) -> str:
        tt = task_list(task_id=task_id)
        if len(tt) > 0:
            for t in tt:  
                t_id = t.get("id")
                return t_id
        else:
            return None

def by_waiting():
    tt = task_list()
    for t in tt:
        t_id = t.get("id")
        task_id = t.get("taskId")
        print(f'查询到任务task_id --> {task_id}, 任务开发者---> {t.get("applicant")}, 任务日期---> {t.get("createTime")}, , 任务主题---> {t.get("topicName")}')
        message = approval(t_id, task_id, approval=approval)
        if message == "操作成功！":
            print(f"task {task_id} 审批成功！")

# def waitApproval(task_id: str):
#     t_id = by_task_id(task_id)
#     message = approval(t_id, task_id, approval=approval)
#     if message == "操作成功！":
#         print(f"task {task_id} 审批成功！")
#     else:

    
def extract(task_id:str) -> dict:
    t_id = by_task_id(task_id)
    data = task_info1(t_id)

    task = data.get('data', {}).get('taskDtoLatest', {}).get('task', {})
    taskName = task.get('taskName')

    task = data.get('data', {}).get('taskDtoLatest', {}).get('map', {})
    sql = task.get("select.sql")

    return {'taskId': task_id, 'taskName': taskName, 'sql': sql}

# def check(task_id:str) -> list:
#     return_list = []
#     t_id = by_task_id(task_id)
#     data = task_info1(t_id)
#     task = data.get('data', {}).get('taskDtoLatest', {}).get('task', {})
#     caution_t = task.get("unSuccessOverTime")
#     start_t = task.get("startDate")
#     # 假设你有一个字符串，格式为 "2022-11-22 03:30:00"
#     # 使用 datetime.strptime() 方法将字符串解析为 datetime 对象
#     date_object = datetime.strptime(start_t, '%Y-%m-%d %H:%M:%S')
#     # 修改时间格式为 "HH:MM"
#     start_t = "{:02d}:{:02d}".format(date_object.hour, date_object.minute)
#     start_t_cmp = date_object.hour * 60 + date_object.minute
#     date_object = datetime.strptime(caution_t, '%H:%M')
#     caution_t_cmp = date_object.hour * 60 + date_object.minute
#     # 条件1
#     if caution_t_cmp <= start_t_cmp:
#         return_list.append("告警时间需晚于生效时间")
#     # 条件2
#     in_charge = task.get("inCharge")
#     my_list = in_charge.split(',')
#     if len(my_list) < 2:
#         return_list.append("任务负责人至少2个")
#     return return_list
        

if __name__ == '__main__':
    # print(by_task_id(10007072))
    # 10007072
    # data = task_info1(60863)
    # # 使用get方法来安全地访问嵌套字典
    # task = data.get('data', {}).get('taskDtoLatest', {}).get('task', {})
    # taskId = task.get('taskId')
    # taskName = task.get('taskName')

    # print(taskId)
    # print(taskName)
    # print(extract(10029188))
    # print(check(10029188))

    approval(10038922,False)

    # # print('-------------------------------------------------')
    
    # data = task_info1(60766)
    # task = data.get('data', {}).get('taskDtoLatest', {}).get('map', {})
    # sql = task.get("select.sql")
    # print(sql)

    # print(extract(60766))

    # print(task_info1(10007072))