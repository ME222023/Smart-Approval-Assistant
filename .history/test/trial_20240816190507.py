import sys
sys.path.append("/home/hezp1/AI/app_weichat")

from interact.admin_interact import getReverseDict, getCusIds, getTaskIdsByUid

dict = getReverseDict()
print(dict)

id_list = getCusIds()
print(id_list)

list = getTaskIdsByUid(dict,'17369c736ab9e12dd4c5fb94e338ff78')
print(list)