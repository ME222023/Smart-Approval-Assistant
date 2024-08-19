import time
import requests
from typing import List


base_url = "http://dispatcher.k8stest.axzq.com.cn"
# 认证token
TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ7XCJ1c2VySWRcIjpcIjIwM1wiLFwidXNlcm5hbWVcIjpcInpoYW5nemg0XCIsXCJuYW1lXCI6XCLlvKDkuonovolcIixcImJ6XCI6XCJOT1JNQUwsQURNSU5cIixcImFkbWluXCI6dHJ1ZSxcImVuYWJsZWRcIjp0cnVlLFwibm9ybVJvbGVJZFwiOlwiXCIsXCJhY2NvdW50Tm9uRXhwaXJlZFwiOnRydWUsXCJhY2NvdW50Tm9uTG9ja2VkXCI6dHJ1ZSxcImNyZWRlbnRpYWxzTm9uRXhwaXJlZFwiOnRydWV9IiwiaXNzIjoiemhhbmd6aDQiLCJpYXQiOjE3MjIyMTQzMjgsImV4cCI6MTcyMjMwMDcyOH0.7pBvz_646QTulPOweHgJFO6DO5kFDVvOSRfyyHLIl9R3KrhIVqjni4a76eJIFJDcwQ2Isca42Nptpu9gUbSt3Q"

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

def approval(t_id:str, task_id:str, approval=True):
    url = f"{base_url}/api/v1/task-approval/approval/{t_id}"
    
    if approval:
        payload = {"approvalComment":"审批通过", "approvalResult":"APPROVAL_PASSED", "taskId": str(task_id)}
    else:
        payload = {"approvalComment":"审批不通过，任务开发者跟进处理！！！","approvalResult":"APPROVAL_NOT_PASSED","taskId": str(task_id)}
    
    print(payload)
    response = requests.post(url, json=payload, headers=HEADERS)
    print(response.json())
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


def by_task_id(task_ids: str, approval=True):
    if len(task_ids) > 0:
        print("通过task_id审批")
        for task_id in task_ids:
            tt = task_list(task_id=task_id)
            # if len(tt) > 0:
            for t in tt:
                t = tt[0]
                t_id = t.get("id")
                print(f'查询到任务task_id --> {task_id}, 任务开发者---> {t.get("applicant")}, 任务日期---> {t.get("createTime")}')
                # message = approval(task_id, approval=approval)
                # if message == "操作成功！":
                #     print(f"task {task_id} 审批成功！")


def by_waiting():
    tt = task_list()
    for t in tt:
        t_id = t.get("id")
        task_id = t.get("taskId")
        print(f'查询到任务task_id --> {task_id}, 任务开发者---> {t.get("applicant")}, 任务日期---> {t.get("createTime")}, , 任务主题---> {t.get("topicName")}')
        message = approval(t_id, task_id, approval=approval)
        if message == "操作成功！":
            print(f"task {task_id} 审批成功！")

def extract(t_id:str) -> dict:
    data = task_info1(t_id)
    task = data.get('data', {}).get('taskDtoLatest', {}).get('task', {})
    taskId = task.get('taskId')
    taskName = task.get('taskName')

    task = data.get('data', {}).get('taskDtoLatest', {}).get('map', {})
    sql = task.get("select.sql")

    return {'taskId': taskId, 'taskName': taskName, 'sql': sql}

if __name__ == '__main__':
    # 10007072
    # data = task_info1(60863)
    # # 使用get方法来安全地访问嵌套字典
    # task = data.get('data', {}).get('taskDtoLatest', {}).get('task', {})
    # taskId = task.get('taskId')
    # taskName = task.get('taskName')

    # print(taskId)
    # print(taskName)
    # print(extract(60863))
    # # print('-------------------------------------------------')
    
    # data = task_info1(60766)
    # task = data.get('data', {}).get('taskDtoLatest', {}).get('map', {})
    # sql = task.get("select.sql")
    # print(sql)

    # print(extract(60766))

    print(task_info1(10007072))