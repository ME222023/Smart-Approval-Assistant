# import configparser

# config = configparser.ConfigParser()

# config.read("/home/hezp1/AI/app_weichat/config.ini")

# print(config.sections())
# print(config.get("server", "admin_list"))

import sys
sys.path.append("/home/hezp1/AI/app_weichat")

from utils.config import Config
from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput
from chat.send_app import qywx
from interact.admin_interact import getWait

config = Config()
config.init("/home/hezp1/AI/app_weichat/config.ini")

admin_ids = config.config['server']['admin_ids']

cus_dict = {
    '16bd52abceae57867cfaa7e4bb9adab4' : 'zhangxs1',
    '17369c736ab9e12dd4c5fb94e338ff78' : 'gongwj'
}

wait_values = getWait()
print(wait_values)
user_list = []
user_set = set()  # 使用集合来避免重复
for u_id in wait_values:
    user_list.append(cus_dict[u_id])
print(user_list)

for u_id in wait_values:
        if u_id in cus_dict:
            user_set.add(cus_dict[u_id])
        else:
            print(f"User ID {u_id} not found in cus_dict")

    user_list = list(user_set)  # 将集合转换为列表
    print(user_list)
# def main():
#     graphviz = GraphvizOutput()
#     graphviz.output_file = 'graph_test.png'

#     with PyCallGraph(output=graphviz):
#         config = Config()
#         config.init("/home/hezp1/AI/app_weichat/config.ini")
#         redis_url = config.redis_url
#         # redis = config.config['server']['redis_url']
#         # token = config.config['server']['token']
#         # admin_list = config.config['server']['admin_ids']
#         # base_url = config.config['server']['base_url']

#         # print(f"redis = {redis}, token = {token}, admin_list = {admin_list}, base_url = {base_url}")
#         print(f"redis = {redis_url}")

# if __name__ == '__main__':
#     main()
