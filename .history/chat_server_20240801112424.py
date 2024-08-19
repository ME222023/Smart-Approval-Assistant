import redis
import time
import json
from LLM.assistant import get_answer
from chat.send_app import qywx
from scheduler.schedule_handle import *
from ruler_handle.rules import *


redis_url = "redis://:123@10.5.5.73:16379/v1"
r = redis.from_url(redis_url)

qw = qywx()

# for k in keys:
#     print(k)

# return_info = combine(10007072)
# return_msg = check(return_info)
# print(return_msg)

def returnMsg(task_id: str, msg: list) -> str:
    # 检查列表中的每一项是否都为 None
    if all(item is None for item in msg):
        return "检测通过，已通知管理员进行审批。"
    # 提取列表中不为 None 的项
    issues = [item for item in msg if item is not None]
    # 构建输出字符串
    output = f"任务{task_id}存在以下问题：\n"
    for index, issue in enumerate(issues, start=1):
        output += f"{index}. {issue}\n"
    
    return output.strip()  # 移除末尾的换行符

def check(tasks_id:list) -> list:
    combined_msgs = []
    for id in tasks_id:
        return_info = combine(id)
        judge_id  = return_info.taskId
        try:
            if not judge_id:
                raise ValueError("Data is empty")
            msg_list = check(return_info)
        except ValueError as e:
            msg_list = ["没有查询到相关的任务，请检查输入的任务ID是否正确"]
        return_msg = returnMsg(id,msg_list)
        combined_msgs.append(return_msg)
    return combined_msgs

while True:
    keys = r.keys()
    for k in keys:
        k = k.decode("utf-8")
        if k.startswith("msg_"):
            msg = r.lpop(k)
            msg = msg.decode("utf-8")
            print(f"用户{k}说了：{msg}")
            data = get_answer(msg)
            print(data)
            try:
                answer = json.loads(data)
                if isinstance(answer, dict):
                    tasks_id = answer.get('tasks_id')
                    print(tasks_id)
                    # tasks_name = answer.get('tasks_name')
                    combined_msgs = []
                    # combined_msgs = check(tasks_id)
                    # print(combined_msgs)
                    # combined_msgs = []
                    for id in tasks_id:
                        return_info = combine(id)
                        print(return_info)
                        judge_id  = return_info.taskId
                        print(judge_id)
                        try:
                            if not judge_id:
                                raise ValueError("Data is empty")
                            msg_list = check(return_info)
                        except ValueError as e:
                            msg_list = ["没有查询到相关的任务，请检查输入的任务ID是否正确"]
                        return_msg = returnMsg(id,msg_list)
                        print()
                        combined_msgs.append(return_msg)
                    qw.send_text("\n\n".join(combined_msgs) + "\n\n请解决以上的问题。", ["17a755177f4ad1f1d99bf8042cfbb74a"])  # 返回内容，用户id
            except json.JSONDecodeError as e:
                qw.send_text(data, ["17a755177f4ad1f1d99bf8042cfbb74a"])
            except PermissionError as e:
                    # 捕获自定义的权限被拒绝异常和系统的权限错误异常
                    # print(f"登录失败: {e}")
                qw.send_text("没有权限登陆失败，请联系管理员进行处理。", ["17a755177f4ad1f1d99bf8042cfbb74a"])
            except MemoryError as e:
                # 捕获 MemoryError 异常并输出异常信息
                qw.send_text("发生了内存错误，请联系管理员进行处理。", ["17a755177f4ad1f1d99bf8042cfbb74a"])
            except SystemExit as e:
                # 捕获 SystemExit 异常并输出异常信息
                qw.send_text("发生了系统退出，请联系管理员进行处理。", ["17a755177f4ad1f1d99bf8042cfbb74a"])
            except KeyboardInterrupt as e:
                # 捕获 KeyboardInterrupt 异常并输出异常信息
                qw.send_text("发生了键盘中断，请联系管理员进行处理。", ["17a755177f4ad1f1d99bf8042cfbb74a"])
            # 捕获所有额外的错误
            except Exception as e:
                qw.send_text("系统出现异常，请联系管理员进行处理。", ["17a755177f4ad1f1d99bf8042cfbb74a"])
    time.sleep(2)
