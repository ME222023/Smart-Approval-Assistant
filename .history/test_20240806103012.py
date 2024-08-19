import redis

def getWait() -> list:
    # Get all keys that match the pattern "wait_*"
    wait_keys = r_.keys("wait_*")
    # Get all values from the keys that match the pattern
    wait_values = []
    for key in wait_keys:
        values = r_.lrange(key, 0, -1)  # Get all values from the list
        wait_values.extend(values)
    return wait_values

def reverse() -> list:
    keys = r_.keys("wait_*")
    # 反转键值对
    reversed_kv_pairs = []
    for key in keys:
        # 获取键对应的列表中的所有值
        values = r_.lrange(key, 0, -1)
        for value in values:
            # 构造反转后的键值对
            reversed_kv_pairs.append((value, f"wait_{value}"))
    return reversed_kv_pairs

# result = getWait()
# print(result)
# reverse()

def waitApprova(tasks_id: list, approval = True):
    wait_tasks = getWait()
    reverse_tasks = reverse()
    for id in tasks_id:
        if id not in wait_tasks:
            # 发送消息给admin：该任务id不存在
        else:
            # 批准通过
            # 发送消息给对应的用户：***任务已经通过审批，请及时查看。
            # 有cus_id
            from_id = reverse_tasks.get(id)
            cus_id = 
            if approval:
                for 
                value = r.get(id)