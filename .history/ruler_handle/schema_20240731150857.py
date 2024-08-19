from pydantic import BaseModel, Field
from typing import Dict, Optional

class scheduleInfo(BaseModel):
    developer: str = Field(None, description="任务开发者")
    sourceTables: str = Field(None, description="任务来源表")
    source_table_name: str = Field(None, alias='source.table.name', description="源表名")
    taskId: str = Field(None, description="任务ID")
    taskType: str = Field(None, description="任务类型")
    taskName: str = Field(None, description="任务名称")
    truncate_sql: str = Field(None, alias='truncate.sql', description="DELETE SQL")
    select_sql: str = Field(None, alias='select.sql', description="查询SQL")
    insert_sql: str = Field(None, alias='insert.sql', description="插入SQL")
    source_database_name: str = Field(None, alias='source.database.name', description="源库名")
    ignore_empty_datasource: str = Field(None, alias='ignore.empty.datasource', description="目标")
    db_table_name: str = Field(None, alias='db.table.name', description="目标表名")
    cycleNum: str = Field(None, description="步长")
    cycleUnit: str = Field(None, description="调度周期")
    startDate: str = Field(None, description="生效时间")
    retriable: str = Field(None, description="是否失败重试")
    selfDepend: str = Field(None, description="是否自依赖")
    taskPriority: str = Field(None, description="优先级")




    brokerIp: str = Field(None, description="代理IP")
    serverTag: str = Field(None, description="服务器标签")
    
    
    
    endDate: str = Field(None, description="结束日期")
    
    taskAction: str = Field(None, description="任务动作")
    tryLimit: str = Field(None, description="重试限制")
    delayTime: str = Field(None, description="延迟时间")
    startupTime: str = Field(None, description="启动时间")
    aliveWait: str = Field(None, description="存活等待时间")
    
    status: str = Field(None, description="状态")
    
    taskGroup: str = Field(None, description="任务组")
    notes: str = Field(None, description="备注")
    
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
    
    hive_database: str = Field(None, alias='hive.database', description="Hive数据库")
    relational_table: str = Field(None, alias='relational.table', description="关系表")
    horaeAlert_check_lines: str = Field(None, alias='horaeAlert.check.lines', description="HoraeAlert检查行数")
    collection_tool_type: str = Field(None, alias='collection.tool.type', description="收集工具类型")
    file_storage_format: str = Field(None, alias='file.storage.format', description="文件存储格式")
    hive_type_check: str = Field(None, alias='hive.type.check', description="Hive类型检查")
    relational_database: str = Field(None, alias='relational.database', description="关系数据库")
    hive_table_name: str = Field(None, alias='hive.table.name', description="Hive表名")
    
    field_json: str = Field(None, alias='field.json', description="字段JSON")
    hive_partition_value: str = Field(None, alias='hive.partition.value', description="Hive分区值")


if __name__ == "__main__":
    
    data = {
        "taskId": "12",
        "taskName": "12",
        "inCharge": "12",
        "startDate": "345",
        # "select.sql":"123",
        "unSuccessOverTime": "12"
    }
    info = scheduleInfo(**data)
    print(info)
