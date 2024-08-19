import ast
from pydantic import BaseModel
from datetime import datetime
from typing import Dict
from schedule_handle import by_task_id, task_info1

class Info(BaseModel):
    taskid: str  
    taskname: str  
    sql: str
    in_charge: str
    start_t: str
    caution_t: str

# rule1: 告警时间需晚于生效时间
def r1(info:dict) -> str:
    task = info.get('data', {}).get('taskDtoLatest', {}).get('task', {})
    caution_t = task.get("unSuccessOverTime")
    start_t = task.get("startDate")
    # 假设你有一个字符串，格式为 "2022-11-22 03:30:00"
    # 使用 datetime.strptime() 方法将字符串解析为 datetime 对象
    date_object = datetime.strptime(start_t, '%Y-%m-%d %H:%M:%S')
    # 修改时间格式为 "HH:MM"
    start_t = "{:02d}:{:02d}".format(date_object.hour, date_object.minute)
    start_t_cmp = date_object.hour * 60 + date_object.minute
    date_object = datetime.strptime(caution_t, '%H:%M')
    caution_t_cmp = date_object.hour * 60 + date_object.minute
    # 条件1
    if caution_t_cmp <= start_t_cmp:
        return "告警时间需晚于生效时间"

# 任务负责人至少2个
def r2(info:dict) -> str:
    task = info.get('data', {}).get('taskDtoLatest', {}).get('task', {})
    in_charge = task.get("inCharge")
    my_list = in_charge.split(',')
    if len(my_list) < 2:
        return "任务负责人至少2个"

def get_function_names(filename):
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)
    
    function_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return function_names

def check(info:dict) -> list:
    filename = __file__  # 获取当前文件名
    functions = get_function_names(filename)
    
    # 排除 'check' 函数自身
    functions = [f for f in functions if f != 'check' and f != 'get_function_names']
    
    res = []

    # 执行提取到的函数
    for name in functions:
        func = globals().get(name)
        if callable(func):
            print(f"Executing {name}()")
            res.append(func(info))
    return res

if __name__ == "__main__":
    t_id = by_task_id(10007072)
    info = task_info1(t_id)
    data1_task = info.get('data', {}).get('taskDtoLatest', {}).get('task', {})
    data1_map = info.get('data', {}).get('taskDtoLatest', {}).get('map', {})
    # print(data1)
    print(type(data1_task))
    print(type(data1_map))
    data2_task = info.get('data', {}).get('taskDtoOlder', {}).get('task', {})
    data2_map = info.get('data', {}).get('taskDtoOlder', {}).get('map', {})
    data_merge1 = data1_task | data1_map
    data_merge1 = {**dict1, **dict2, **dict3}

    # data_merge2 = data2_task | data2_map

    print(data_merge1)
    # print(data_merge2)

    # print(check(info))