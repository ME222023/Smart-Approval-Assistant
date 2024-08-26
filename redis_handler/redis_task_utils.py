from collections import defaultdict
from typing import List

from utils.config import Config
from redis_handler.redis_handle import RedisClient

def get_cus_ids() -> List[str]:
    """
    取出(waitt_{task_ID},cus_ID)中cus_ID的列表
    @return: 返回cus_ID的列表
    """
    # 取键名称
    with RedisClient(Config.redis_url) as client: 
        wait_keys = client.keys("waitt_*")
    wait_values = []
    # 取键对应的值
    for key in wait_keys:
        with RedisClient(Config.redis_url) as client: 
            byte_values = client.lrange(key, 0, -1)  # Get all values from the list
        str_values = [value.decode('utf-8') for value in byte_values]
        # 将转换后的值添加到 wait_values 列表中
        wait_values.extend(str_values)
    return wait_values

def get_cus_name_list() -> List[str]:
    """
    得到cus_ID对应的cus_name列表
    @return: 返回元素不重复的cus_name列表
    """
    wait_values = get_cus_ids()
    cus_list = []
    cus_set = set()  # 使用集合来避免重复
    for u_id in wait_values:
        u_name = Config.get_uid_uname(u_id)
        if u_name:
            cus_set.add(u_name)
    cus_list = list(cus_set)  # 将集合转换为列表
    return cus_list

def get_taskid_cusid_dict() -> dict:
    """
    获取所有匹配模式 "waitt_*" 的键值对，并返回 {task_id: cus_id} 形式的字典
    @return: 返回{task_id: cus_id} 形式的字典
    """
    result = {}
    with RedisClient(Config.redis_url) as client: 
        wait_keys = client.keys("waitt_*")
    for key in wait_keys:
        task_id = key.decode('utf-8').split('_')[1]  
        with RedisClient(Config.redis_url) as client:
            byte_values = client.lrange(key, 0, -1)  
        str_values = [value.decode('utf-8') for value in byte_values]
        if str_values:
            result[task_id] = str_values[0]
    return result

def get_cusid_taskid_dict() -> dict:
    """
    获取所有匹配模式 "waitt_*" 的键值对，并返回 {cus_id: task_id} 形式的字典
    @return: 返回{cus_id: task_id} 形式的字典
    """
    with RedisClient(Config.redis_url) as client: 
        keys = client.keys("waitt_*")
    # 反转键值对
    reversed_kv_pairs = defaultdict(list)
    for key in keys:
        # 获取键对应的列表中的所有值
        with RedisClient(Config.redis_url) as client: 
            values = client.lrange(key, 0, -1)
        for value in values:
            value = value.decode('utf-8')
            reversed_kv_pairs[value].append(key.decode('utf-8').replace('waitt_', ''))
    return reversed_kv_pairs

    
def get_taskid_list() -> List[str]:
    """
    获取所有匹配模式 "waitt_*" 的键，并返回task_id组成的列表
    @return: 返回(waitt_{task_id},cus_id)中task_id组成的列表
    """
    with RedisClient(Config.redis_url) as client: 
        tasks_id = [key.decode("utf-8").split('_')[-1] for key in client.keys('waitt_*')]
    return tasks_id