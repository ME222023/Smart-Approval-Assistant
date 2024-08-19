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


while True:
    keys = r.keys()
    for k in keys:
        k = k.decode("utf-8")
        if k.startswith("msg_"):
            msg = r.lpop(k)
            if msg is not None:
                if
                msg = msg.decode("utf-8")
                print(f"用户{k}说了：{msg}")
                data = get_answer(msg)
                try:
                #     # 检查 data 是否为空
                #     if not data:
                #         raise ValueError("Data is empty")
                    
                #     # 如果 data 不为空，继续处理
                #     print("Data received:", data)
                    
                # except ValueError as e:
                #     # 捕获 ValueError 异常并输出 "fail"
                #     print("fail")
                #     qw.send_text("没有查询到相关的任务，请检查输入的任务ID是否正确。", ["17a755177f4ad1f1d99bf8042cfbb74a"])
                    try:
                        answer = json.loads(data)
                        if isinstance(answer, dict):
                            # print(answer)
                            tasks_id = answer.get('tasks_id')
                            tasks_name = answer.get('tasks_name')
                            # print(tasks_id)
                            # print(tasks_name)
                            # 通过task_id和task_name查询
                            combined_msgs = []
                            for id in tasks_id:
                                #return_msg = extract(id)
                                return_info = combine(id)
                                judge_id  = return_info.taskId
                                # print(return_info)
                                try:
                                    if not judge_id:
                                        # print("error: Data is empty")
                                        raise ValueError("Data is empty")
                                        # 如果 data 不为空，继续处理                                        
                                    # print("Data received:", data)
                                    # print(return_info)
                                    # print(type(return_info))
                                    # return_info = scheduleInfo(**info)
                                    msg_list = check(return_info)
                                    # print(return_msg)
                                    # print(type(return_msg))
                                    # 对return_msg进行一系列操作
                                    # 返回审核的结果
                                    # print(return_msg)
                                    # return_msg = json.dumps(return_msg, ensure_ascii=False)
                                    # 返回到微信客户端
                                except ValueError as e:
                                    # 捕获 ValueError 异常并输出 "fail"
                                    # print("fail")
                                    msg_list = ["没有查询到相关的任务，请检查输入的任务ID是否正确"]
                                return_msg = returnMsg(id,msg_list)
                                combined_msgs.append(return_msg)
                            qw.send_text("\n\n".join(combined_msgs) + "\n\n请解决以上的问题。", ["17a755177f4ad1f1d99bf8042cfbb74a"])  # 返回内容，用户id
                    except json.JSONDecodeError as e:
                        qw.send_text(data, ["17a755177f4ad1f1d99bf8042cfbb74a"])
                except PermissionError as e:
                    # 捕获自定义的权限被拒绝异常和系统的权限错误异常
                    # print(f"登录失败: {e}")
                    qw.send_text("没有权限登陆失败，请联系管理员进行处理。", ["17a755177f4ad1f1d99bf8042cfbb74a"])
                except ValueError as e:
                    # 捕获 ValueError 异常并输出 "fail"
                    print("fail")
                    qw.send_text("请输入信息。", ["17a755177f4ad1f1d99bf8042cfbb74a"])
                except MemoryError as e:
                    # 捕获 MemoryError 异常并输出异常信息
                    print(f"MemoryError occurred: {e}")
                except SystemExit as e:
                    # 捕获 SystemExit 异常并输出异常信息
                    print(f"SystemExit occurred: {e}")
                    raise  # 重新引发 SystemExit 异常以退出程序
                except KeyboardInterrupt as e:
                    # 捕获 KeyboardInterrupt 异常并输出异常信息
                    print(f"KeyboardInterrupt occurred: {e}")
                    raise  # 重新引发 KeyboardInterrupt 异常以允许正常中断程序
                finally:
                    # 无论是否发生异常，这部分代码都会执行
                    qw.send_text("系统出现异常，请联系管理员进行处理。", ["17a755177f4ad1f1d99bf8042cfbb74a"])
                # except Exception as e:
                #     # 捕获其他所有异常并输出异常信息
                #     print(f"An unexpected error occurred: {e}")
                #     qw.send_text("系统出现异常，请联系管理员进行处理。", ["17a755177f4ad1f1d99bf8042cfbb74a"])
            else:
                print("message is empty.")
    time.sleep(2)
