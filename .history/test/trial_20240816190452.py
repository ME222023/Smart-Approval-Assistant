import sys
sys.path.append("/home/hezp1/AI/app_weichat")

from interact.admin_interact import getReverseDict, getCusIds, getTaskIdsByUid

dict = getReverseDict()
print(dict)

id_list = getCusIds()
print(id_list)

getTaskIdsByUid(dict,)