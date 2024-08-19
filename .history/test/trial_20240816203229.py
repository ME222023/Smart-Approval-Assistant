import sys
sys.path.append("/home/hezp1/AI/app_weichat")

from interact.admin_interact import getReverseDict, printAprroval,updateTaskStatus

# namelist = getCusNameList()
# print(namelist)

# id_list = getCusIds()
# print(id_list)

dict = getReverseDict()
print(dict)

# list = getTaskIdsByUid(dict,'zhangxs1')
# print(list)

dict1 = updateTaskStatus(dict,'zhangxs1',"通过")
print(dict1)

# cusName2cusId = {
#     'zhangxs1' : '16bd52abceae57867cfaa7e4bb9adab4',
#     'gongwj' : '17369c736ab9e12dd4c5fb94e338ff78' 
# }

# id = cusName2cusId['']
# print(id)