import sys
sys.path.append("/home/hezp1/AI/app_weichat")

from interact.admin_interact import getTaskUserIdDict,getCusNameList,getCusIds,getReverseDict, printAprroval,updateTaskStatus

dict1 = getTaskUserIdDict()
# namelist = getCusNameList()
# print(namelist)

# id_list = getCusIds()
# print(id_list)

# dict = getReverseDict()
# print(dict)

# list = getTaskIdsByUid(dict,'zhangxs1')
# print(list)

# dict1 = updateTaskStatus(dict,'jjs',"不通过")
# print("--------------------------")
# print(dict1)

# printAprroval(dict1)

# cusName2cusId = {
#     'zhangxs1' : '16bd52abceae57867cfaa7e4bb9adab4',
#     'gongwj' : '17369c736ab9e12dd4c5fb94e338ff78' 
# }

# id = cusName2cusId['']
# print(id)