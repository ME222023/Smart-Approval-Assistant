import sys
sys.path.append("/home/hezp1/AI/app_weichat")

from interaction_handler.admin_interact_handle import get_taskid_cusid_dict

# from chat.send_app import qywx
# from scheduler.schedule_handle import getTaskList,getInfoByUser,getApplicantId
# from utils.get_handle import getCusIds, getCusNameList
# from scheduler.schedule_handle import getLatestTaskInfo, getTId
# from ruler_handle.rules import checkRules

# info = getLatestTaskInfo("10031408")
# print(info)

# return_info = getLatestTaskInfo("10031408")
# print(checkRules(return_info,'16bd52abceae57867cfaa7e4bb9adab4'))

dict = get_taskid_cusid_dict()
print(dict)


# test：u_id <--> name
# cusId2cusName = {
#     '16bd52abceae57867cfaa7e4bb9adab4' : 'zhangxs1',
#     '17369c736ab9e12dd4c5fb94e338ff78' : 'gongwj',
#     '1730846d950e0a5709ac2ea44138df09' : 'zhangqi5',
#     '17a755177f4ad1f1d99bf8042cfbb74a' : 'zhangzh4'
# }
# cusName2cusId = {
#     'zhangxs1' : '16bd52abceae57867cfaa7e4bb9adab4',
#     'gongwj' : '17369c736ab9e12dd4c5fb94e338ff78',
#     'zhangqi5' : '1730846d950e0a5709ac2ea44138df09',
#     'zhangzh4' : '17a755177f4ad1f1d99bf8042cfbb74a' 
# }


# print(getApplicantId('10031415'))

# print(cusId2cusName[''])
# print(getCusIds())
# print(getCusNameList())

# print(getTaskList("","lixh6"))
# print(getInfoByUser("lixh6"))

# task_list = getInfoByUser("lixh6")
# print(task_list)

# print(getApplicantId("10039111"))
# print(getApplicantId("100"))
# qw = qywx()

# qw.send_text("123456", [""])

# dict2 = getTaskUserIdDict()
# print(dict2)
# print(dict2['10037085'])
# print(type(dict2['10037085']))

# dict1 = getTaskUserIdDict()
# print(dict1)

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