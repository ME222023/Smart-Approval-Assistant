import sys
sys.path.append("/home/hezp1/AI/app_weichat")

from interact.admin_interact import getReverseDict, getCusIds, getTaskIdsByUid,getCusNameList

namelist = getCusNameList()
print(namelist)

dict = getReverseDict()
print(dict)

id_list = getCusIds()
print(id_list)

list = getTaskIdsByUid(dict,'zhangxs1')
print(list)

# cusName2cusId = {
#     'zhangxs1' : '16bd52abceae57867cfaa7e4bb9adab4',
#     'gongwj' : '17369c736ab9e12dd4c5fb94e338ff78' 
# }

# id = cusName2cusId['']
# print(id)