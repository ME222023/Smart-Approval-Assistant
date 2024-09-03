# import pandas as pd

# df = pd.read_csv("/home/hezp1/AI/app_weichat/oa.csv")

# def getNameIdList(uid: str = None, uname: str = None) -> list:
#     if uid:
#         uname = df[df["emp_id"].str.contains(uid)]
#         return uname["emp_oa"].values
#     if uname:
#         u_id = df[df["emp_oa"].str.contains(uname)]
#         return u_id["emp_id"].values

# print(getNameIdList("17a755177f4ad1f1d99bf8042cfbb74a"))
# print(getNameIdList(None,"zhangzh4"))
# uname = df[df["emp_id"].str.contains("17a755177f4ad1f1d99bf8042cfbb74a")]
# print(uname["emp_oa"].values)

# import sys
# sys.path.append("/home/hezp1/AI/app_weichat")

# msg = [None, None, '请求任务审批者需是任务开发者或任务负责人。']
# if all(item is None for item in msg):
#     print("pass the check")
# else:
#     print("no!!")

from interaction_handler.cus_interact_handle import check_task_id

info = check_task_id("zhangxs1","16bd52abceae57867cfaa7e4bb9adab4")
get_tid
print(info)




# from utils.config import Config
# from test.test2 import shwoa

# shwo = shwoa()

# def get_values_from_dict(input_str, dictionary):
#     # 将输入字符串按 '|' 分割成键列表
#     keys = input_str.split('|')
    
#     # 根据键从字典中获取相应的值
#     values = [dictionary[key] for key in keys if key in dictionary]
    
#     # 将值列表按 '|' 连接成字符串
#     result = '|'.join(values)
    
#     return result

# # 示例字典
# dict = {"zhangzh4": "17a755177f4ad1f1d99bf8042cfbb74a", "zhangqi5":"1730846d950e0a5709ac2ea44138df09"}

# # 输入字符串
# input_str = "a|b"

# # 调用函数并输出结果
# output_str = get_values_from_dict(input_str, dict)
# print(output_str)  # 输出：17a755177f4ad1f1d99bf8042cfbb74a|1730846d950e0a5709ac2ea44138df09


# from scheduler.schedule_handle import approval

# approval("14110")


# Config.init("config.ini","oa.csv")

# print(Config.base_url)
# redis_url = config.redis_url
# admin_ids = config.admin_ids
# name_list = config.getNameList()

# # print(name_list)

# # print(redis_url)
# # print(admin_ids)

# print(config.getNameIdList("17a755177f4ad1f1d99bf8042cfbb74a"))
# print(type(config.getNameIdList("17a755177f4ad1f1d99bf8042cfbb74a")))
