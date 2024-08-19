import ast
import json
from pydantic import BaseModel, Field
from datetime import datetime
from scheduler.schedule_handle import by_task_id, task_info1
from ruler_handle.schema import scheduleInfo

# rule1: 告警时间需晚于生效时间
def r1(info:dict) -> str:
    # task = info.get('data', {}).get('taskDtoLatest', {}).get('task', {})
    caution_t = info.get("unSuccessOverTime")
    start_t = info.get("startDate")
    print(caution_t)
    print(start_t)
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
    # task = info.get('data', {}).get('taskDtoLatest', {}).get('task', {})
    in_charge = info.get("inCharge")
    # in_charge = info.inCharge
    my_list = in_charge.split(',')
    if len(my_list) < 2:
        return "任务负责人至少2个"

def get_function_names(filename):
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)
    
    function_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return function_names

def check(info:scheduleInfo) -> list:
    filename = __file__  # 获取当前文件名
    functions = get_function_names(filename)
    
    # 排除 'check' 函数自身
    functions = [f for f in functions if f != 'check' and f != 'get_function_names']
    
    res = []

    print(type(info.dict()))
    print(info.dict())
    r1(info.dict())

    # 执行提取到的函数
    # for name in functions:
    #     func = globals().get(name)
    #     if callable(func):
    #         # print(f"Executing {name}()")
    #         res.append(func(info.dict()))
    return []

def combine(task_id:str) -> scheduleInfo:
    t_id = by_task_id(task_id)
    info = task_info1(t_id)
    data_task = info.get('data', {}).get('taskDtoLatest', {}).get('task', {})
    data_map = info.get('data', {}).get('taskDtoLatest', {}).get('map', {})
    data_merge = {**data_task, **data_map}
    json_str = json.dumps(data_merge, ensure_ascii=False, indent=4)
    json_obj = json.loads(json_str)
    info_instance = scheduleInfo(**json_obj)
    return info_instance

if __name__ == "__main__":
    # t_id = by_task_id(10007072)
    # t_id = by_task_id(10037258)
    # info = task_info1(t_id)
    # data1_task = info.get('data', {}).get('taskDtoLatest', {}).get('task', {})
    # data1_map = info.get('data', {}).get('taskDtoLatest', {}).get('map', {})
    # # data2_task = info.get('data', {}).get('taskDtoOlder', {}).get('task', {})
    # # data2_map = info.get('data', {}).get('taskDtoOlder', {}).get('map', {})
    # data_merge1 = {**data1_task, **data1_map}
    # # data_merge2 = {**data2_task, **data2_map}
    
    data_merge1 = combine(10037258)

    print(data_merge1)
    # print(data_merge2)

    # 将合并后的字典转换为 JSON 字符串
    json_str1 = json.dumps(data_merge1, ensure_ascii=False, indent=4)
    # json_str2 = json.dumps(data_merge2, ensure_ascii=False, indent=4)

    # 将 JSON 字符串转换为 JSON 对象
    json_obj1 = json.loads(json_str1)
    # json_obj2 = json.loads(json_str2)

    # 取对象实例
    print("-------------------------------------------------")
    print("-------------------------------------------------")

    info_instance = scheduleInfo(**json_obj1)
    print(info_instance)

    # print(check(info))