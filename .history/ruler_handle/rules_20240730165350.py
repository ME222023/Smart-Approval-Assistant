import ast
import json
from pydantic import BaseModel, Field
from datetime import datetime
from schedule_handle import by_task_id, task_info1

class Info(BaseModel):
    taskId: str = Field(None, description="任务ID")
    taskType: str = Field(None, description="任务类型")
    taskName: str = Field(None, description="任务名称")
    brokerIp: str = Field(None, description="代理IP")
    serverTag: str = Field(None, description="服务器标签")
    cycleUnit: str = Field(None, description="周期单位")
    cycleNum: str = Field(None, description="周期数")
    startDate: str = Field(None, description="开始日期")
    endDate: str = Field(None, description="结束日期")
    selfDepend: str = Field(None, description="自依赖")
    taskAction: str = Field(None, description="任务动作")
    tryLimit: str = Field(None, description="重试限制")
    delayTime: str = Field(None, description="延迟时间")
    startupTime: str = Field(None, description="启动时间")
    aliveWait: str = Field(None, description="存活等待时间")
    retriable: str = Field(None, description="可重试")
    status: str = Field(None, description="状态")
    taskPriority: str = Field(None, description="任务优先级")
    taskGroup: str = Field(None, description="任务组")
    notes: str = Field(None, description="备注")
    inCharge: str = Field(None, description="负责人")
    createTime: str = Field(None, description="创建时间")
    lastUpdate: str = Field(None, description="最后更新时间")
    oldId: str = Field(None, description="旧ID")
    sourceServer: str = Field(None, description="来源服务器")
    targetServer: str = Field(None, description="目标服务器")
    topicName: str = Field(None, description="主题名称")
    moduleName: str = Field(None, description="模块名称")
    runOverTime: str = Field(None, description="运行超时时间")
    unSuccessOverTime: str = Field(None, description="不成功超时时间")
    scheduleType: str = Field(None, description="调度类型")
    dataType: str = Field(None, description="数据类型")
    taskDesc: str = Field(None, description="任务描述")
    updateBy: str = Field(None, description="更新者")
    upddateDate: str = Field(None, alias='upddateDate', description="更新日期")
    unRunOverTime: str = Field(None, description="未运行超时时间")
    advanceInit: str = Field(None, description="提前初始化")
    developer: str = Field(None, description="开发者")
    sourceTables: str = Field(None, description="源表")
    aitTables: str = Field(None, description="AIT表")
    exeEnvironment: str = Field(None, description="执行环境")
    exec_script_type: str = Field(None, alias='exec.script.type', description="执行脚本类型")
    task_relation: str = Field(None, alias='task_relation', description="任务关系")
    monitorPlatform_access: str = Field(None, alias='monitorPlatform.access', description="监控平台访问")
    approval: str = Field(None, description="审批")
    approval_status: str = Field(None, alias='approval.status', description="审批状态")
    version_timestamp: str = Field(None, description="版本时间戳")
    timeout_early_warning: str = Field(None, alias='timeout.early.warning', description="超时预警")
    data_date_type: str = Field(None, alias='data.date.type', description="数据日期类型")
    applicant: str = Field(None, description="申请人")
    applicant_time: str = Field(None, alias='applicant.time', description="申请时间")
    approval_comment: str = Field(None, alias='approval.comment', description="审批评论")
    skip_festival: str = Field(None, alias='skip.festival', description="跳过节日")
    exec_script_path: str = Field(None, alias='exec.script.path', description="执行脚本路径")
    exec_script_parms: str = Field(None, alias='exec.script.parms', description="执行脚本参数")
    exec_user_name: str = Field(None, alias='exec.user.name', description="执行用户名称")
    skip_weeken: str = Field(None, alias='skip.weeken', description="跳过周末")
    unsuccessful_early_warning: str = Field(None, alias='unsuccessful.early.warning', description="不成功预警")
    approval_result: str = Field(None, alias='approval.result', description="审批结果")
    ignore_empty_datasource: str = Field(None, alias='ignore.empty.datasource', description="忽略空数据源")
    hive_database: str = Field(None, alias='hive.database', description="Hive数据库")
    relational_table: str = Field(None, alias='relational.table', description="关系表")
    horaeAlert_check_lines: str = Field(None, alias='horaeAlert.check.lines', description="HoraeAlert检查行数")
    collection_tool_type: str = Field(None, alias='collection.tool.type', description="收集工具类型")
    file_storage_format: str = Field(None, alias='file.storage.format', description="文件存储格式")
    hive_type_check: str = Field(None, alias='hive.type.check', description="Hive类型检查")
    ignore_empty_datasource1: str = Field(None, alias='ignore.empty.datasource1', description="忽略空数据源1")
    relational_database: str = Field(None, alias='relational.database', description="关系数据库")
    hive_table_name: str = Field(None, alias='hive.table.name', description="Hive表名")
    select_sql: str = Field(None, alias='select.sql', description="选择SQL")
    field_map_json: str = Field(None, alias='field.map.json', description="字段映射JSON")
    hive_partition_value: str = Field(None, alias='hive.partition.value', description="Hive分区值")
    field_json: str = Field(None, alias='field.json', description="字段JSON")

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
            # print(f"Executing {name}()")
            res.append(func(info))
    return res

if __name__ == "__main__":
    # t_id = by_task_id(10007072)
    t_id = by_task_id(10038360)
    info = task_info1(t_id)
    data1_task = info.get('data', {}).get('taskDtoLatest', {}).get('task', {})
    data1_map = info.get('data', {}).get('taskDtoLatest', {}).get('map', {})
    # data2_task = info.get('data', {}).get('taskDtoOlder', {}).get('task', {})
    # data2_map = info.get('data', {}).get('taskDtoOlder', {}).get('map', {})
    data_merge1 = {**data1_task, **data1_map}
    # data_merge2 = {**data2_task, **data2_map}

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
    info_instance = Info(**json_obj1)
    print(info_instance)

    # print(check(info))