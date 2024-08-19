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

config = Config()
config.init("/home/hezp1/AI/app_weichat/config.ini")

admin_ids1 = config.config['server']['admin_ids']
admin_ids2=["17a755177f4ad1f1d99bf8042cfbb74a","1730846d950e0a5709ac2ea44138df09"]

print(admin_ids1)
print(admin_ids1 == admin_ids2)

# admin_ids = [
#     "17a755177f4ad1f1d99bf8042cfbb74a",
#     "1730846d950e0a5709ac2ea44138df09"
# ]
# admin = "|".join(admin_ids1)
qw = qywx()

qw.send_text("待审批任务列表为空，暂时没有可以审批的任务。\n", [admin])

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
