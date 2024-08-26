import ast
from datetime import datetime
from typing import List


from rule_handler.schema import ScheduleInfo
from utils.config import Config


def rule1(info: dict, cus_id: str) -> str:
    """
    检查告警时间是否晚于生效时间
    @param info: 字典格式的调度信息
    @param cus_id: 用户ID（可选）
    若不满足rule1，返回"告警时间需晚于生效时间"的字符串
    """
    caution_t = info.get("unSuccessOverTime")
    start_t = info.get("startDate")
    # 假设你有一个字符串，格式为 "2022-11-22 03:30:00"
    # 使用 datetime.strptime() 方法将字符串解析为 datetime 对象
    date_object = datetime.strptime(start_t, '%Y-%m-%d %H:%M:%S')
    # 修改时间格式为 "HH:MM"
    start_t = "{:02d}:{:02d}".format(date_object.hour, date_object.minute)
    start_t_cmp = date_object.hour * 60 + date_object.minute

    date_object = datetime.strptime(caution_t, '%H:%M')
    caution_t_cmp = date_object.hour * 60 + date_object.minute
    # rule1: 告警时间需晚于生效时间
    if caution_t_cmp < start_t_cmp:
        return "告警时间需晚于生效时间。"

def rule2(info: dict, cus_id: str) -> str:
    """
    检查任务负责人至少2个
    @param info: 字典格式的调度信息
    @param cus_id: 用户ID（可选）
    若不满足rule2，返回"任务负责人至少2个"的字符串
    """
    in_charge = info.get("inCharge")
    my_list = in_charge.split(',')
    # rule2：任务负责人至少2个
    if len(my_list) < 2:
        return "任务负责人至少2个。"
    
def rule3(info: dict, cus_id: str) -> str:
    """
    检查请求任务审批者需是任务开发者或任务负责人
    @param info: 字典格式的调度信息
    @param cus_id: 用户ID
    若不满足rule3，返回"请求任务审批者需是任务开发者或任务负责人"的字符串
    """
    cus_name = Config.get_uid_uname(cus_id)
    if not cus_name:
        return None
    else:
        in_charge = info.get("inCharge")
        developer = info.get("developer")
        my_list = in_charge.split(',')
        my_list.append(developer)
        # rule3：请求任务审批者需是任务开发者或任务负责人
        if cus_name not in my_list:
            return "请求任务审批者需是任务开发者或任务负责人。"

def get_func_names(filename: str) -> List[str]:
    """
    获得rules.py中所有函数的名称列表
    @param cus_id: 文件名称
    返回rules.py文件中函数名称列表
    """
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)
    
    function_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return function_names

def check_rules(info: ScheduleInfo, cus_id: str) -> List[str]:
    """
    返回规则判断后的列表
    @param info: 调度信息
    @param cus_id: 用户申请者ID
    @return: 返回调度信息
    """
    filename = __file__  # 获取当前文件名
    functions = get_func_names(filename)
    
    # 排除'checkRules'和'getFuncNames'函数（不是规则的函数）
    functions = [f for f in functions if f != 'check_rules' and f != 'get_func_names']
    
    res = []

    # 执行提取到的函数
    for name in functions:
        func = globals().get(name)
        if callable(func):
            res.append(func(info.dict(),cus_id))
    return res