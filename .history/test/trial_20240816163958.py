cus_status = {
    'adminA_id': [{'task1_id': "通过", 'task2_id': "不通过"}],
    'adminB_id': [{'task3_id': "通过"}]
}

# 假设你要查找的是 adminA_id
admin_id = 'adminA_id'

# 获取任务ID列表
if admin_id in cus_status:
    task_list = []
    for task_dict in cus_status[admin_id]:
        task_list.extend(task_dict.keys())
    print(task_list)
else:
    print(f"Admin ID {admin_id} not found in cus_status")
