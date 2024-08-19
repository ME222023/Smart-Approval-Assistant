# 将 JSON 字符串解析为 Python 字典
data_1 = json.loads(json_data_1)
data_2 = json.loads(json_data_2)

def compare_dicts(dict1, dict2, path="root"):
    differences = []
    keys1 = set(dict1.keys())
    keys2 = set(dict2.keys())
    
    # 找出 dict1 中有但 dict2 中没有的键
    for key in keys1 - keys2:
        differences.append(f"{path}.{key} is only in the first JSON.")
    
    # 找出 dict2 中有但 dict1 中没有的键
    for key in keys2 - keys1:
        differences.append(f"{path}.{key} is only in the second JSON.")
    
    # 比较相同的键
    for key in keys1 & keys2:
        if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            differences.extend(compare_dicts(dict1[key], dict2[key], f"{path}.{key}"))
        elif dict1[key] != dict2[key]:
            differences.append(f"{path}.{key} differs: {dict1[key]} vs {dict2[key]}")
    
    return differences

# 比较两份 JSON 数据
differences = compare_dicts(data_1, data_2)

# 打印差异
if differences:
    print("Differences found:")
    for diff in differences:
        print(diff)
else:
    print("The two JSON data are identical in structure and values.")




{
    "code": 0,
    "message": "操作成功！",
    "data": {
        "taskDtoLatest": {
            "task": {
                "taskId": "10038986",
                "taskType": "24",
                "taskName": "JXETG_DMB_v_alne_ass_brch_dtl_trd_coll",
                "brokerIp": "any",
                "serverTag": null,
                "cycleUnit": "D",
                "cycleNum": "1",
                "startDate": "2023-12-05 02:00:00",
                "endDate": null,
                "selfDepend": "2",
                "taskAction": "no action at this time",
                "tryLimit": "3",
                "delayTime": "0",
                "startupTime": "120",
                "aliveWait": "30",
                "retriable": "1",
                "status": "W",
                "taskPriority": "4",
                "taskGroup": null,
                "notes": null,
                "inCharge": "huangpeng",
                "createTime": "2024-08-05 11:26:01",
                "lastUpdate": "2024-08-05 11:26:01",
                "oldId": null,
                "sourceServer": "hive",
                "targetServer": "10.5.2.125-jxetg-amos",
                "topicName": "ods_jxetg",
                "moduleName": "",
                "runOverTime": "0",
                "unSuccessOverTime": "03:00",
                "scheduleType": "0",
                "dataType": "0",
                "taskDesc": "交易运营-每月独立考核明细交易数据视图",
                "updateBy": null,
                "upddateDate": "2024-08-05 11:26:01",
                "unRunOverTime": "0",
                "advanceInit": "0",
                "developer": "huangpeng",
                "sourceTables": "v_alne_ass_brch_dtl_trd_coll",
                "aitTables": "DMB_v_alne_ass_brch_dtl_trd_coll",
                "exeEnvironment": "1"
            },
            "map": {
                "task_relation": "",
                "db.database.name": "TSOS",
                "ignore.empty.datasource": "hive",
                "hive.table.name": "v_alne_ass_brch_dtl_trd_coll",
                "select.sql": "select trd_mth, \ntrd_type,\nass_ins_name,\nass_ins_num,\nchn_clas_name,\npd_name,\nnet_ast_scal,\ntrd_amt,\ntrd_net_cms  from  dm_tg.DMB_v_alne_ass_brch_dtl_trd_coll\n where trd_mth='${yyyyMM}';",
                "monitorPlatform.access": "1",
                "approval": "",
                "hive.database": "dm_tg",
                "approval.status": "W",
                "timeout.early.warning": "0",
                "data.date.type": "0",
                "applicant": "huangpeng",
                "applicant.time": "",
                "approval.comment": "",
                "truncate.sql": "delete from tsos.DMB_DMB_v_alne_ass_brch_dtl_trd_coll where trd_mth='${yyyyMM}';",
                "hive.partition.value": "",
                "load.mode": "append",
                "exec.script.parms": "${YYYYMMDD}",
                "ignore.empty.datasource1": "10.5.2.125-jxetg-amos",
                "insert.sql": "insert into tsos.DMB_v_alne_ass_brch_dtl_trd_coll(trd_mth,trd_type,ass_ins_name,ass_ins_num,chn_clas_name,pd_name,net_ast_scal,trd_amt,trd_net_cms) values (?,?,?,?,?,?,?,?,?);",
                "db.table.name": "DMB_v_alne_ass_brch_dtl_trd_coll",
                "unsuccessful.early.warning": "00:00",
                "approval.result": ""
            }
        },
        "taskDtoOlder": {
            "task": {
                "taskId": "10038986",
                "taskType": "24",
                "taskName": "JXETG_DMB_v_alne_ass_brch_dtl_trd_coll",
                "brokerIp": "any",
                "serverTag": null,
                "cycleUnit": "D",
                "cycleNum": "1",
                "startDate": "2023-12-05 02:00:00",
                "endDate": null,
                "selfDepend": "2",
                "taskAction": "no action at this time",
                "tryLimit": "3",
                "delayTime": "0",
                "startupTime": "120",
                "aliveWait": "30",
                "retriable": "1",
                "status": "W",
                "taskPriority": "4",
                "taskGroup": null,
                "notes": null,
                "inCharge": "huangpeng",
                "createTime": "2024-08-05 09:19:22",
                "lastUpdate": "2024-08-05 09:19:21",
                "oldId": null,
                "sourceServer": "hive",
                "targetServer": "10.5.2.125-jxetg-amos",
                "topicName": "ods_jxetg",
                "moduleName": "",
                "runOverTime": "0",
                "unSuccessOverTime": "03:00",
                "scheduleType": "0",
                "dataType": "0",
                "taskDesc": "交易运营-每月独立考核明细交易数据视图",
                "updateBy": null,
                "upddateDate": "2024-08-05 09:19:22",
                "unRunOverTime": "0",
                "advanceInit": "0",
                "developer": "huangpeng",
                "sourceTables": "v_alne_ass_brch_dtl_trd_coll",
                "aitTables": "DMB_v_alne_ass_brch_dtl_trd_coll",
                "exeEnvironment": "1"
            },
            "map": {
                "task_relation": "",
                "db.database.name": "TSOS",
                "ignore.empty.datasource": "hive",
                "hive.table.name": "v_alne_ass_brch_dtl_trd_coll",
                "select.sql": "select trd_mth, \ntrd_type,\nass_ins_name,\nass_ins_num,\nchn_clas_name,\npd_name,\nnet_ast_scal,\ntrd_amt,\ntrd_net_cms  from  dm_tg.DMB_v_alne_ass_brch_dtl_trd_coll\n where trd_mth='${yyyyMM}';",
                "monitorPlatform.access": "1",
                "approval": "",
                "hive.database": "dm_tg",
                "approval.status": "W",
                "timeout.early.warning": "0",
                "data.date.type": "0",
                "applicant": "huangpeng",
                "applicant.time": "",
                "approval.comment": "",
                "truncate.sql": "delete from tsos.DMB_DMB_v_alne_ass_brch_dtl_trd_coll where trd_mth='${yyyyMM}';",
                "hive.partition.value": "",
                "load.mode": "append",
                "exec.script.parms": "${YYYYMMDD}",
                "ignore.empty.datasource1": "10.5.2.125-jxetg-amos",
                "insert.sql": "insert into tsos.DMB_DMB_v_alne_ass_brch_dtl_trd_coll(trd_mth,trd_type,ass_ins_name,ass_ins_num,chn_clas_name,pd_name,net_ast_scal,trd_amt,trd_net_cms) values (?,?,?,?,?,?,?,?,?);",
                "db.table.name": "DMB_v_alne_ass_brch_dtl_trd_coll",
                "unsuccessful.early.warning": "00:00",
                "approval.result": ""
            }
        }
    }
}