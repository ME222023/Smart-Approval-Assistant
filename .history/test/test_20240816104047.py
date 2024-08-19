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

config = Config()
config.init("/home/hezp1/AI/app_weichat/config.ini")
redis_url = config.redis_url
# redis = config.config['server']['redis_url']
# token = config.config['server']['token']
# admin_list = config.config['server']['admin_ids']
# base_url = config.config['server']['base_url']

# print(f"redis = {redis}, token = {token}, admin_list = {admin_list}, base_url = {base_url}")
print(f"redis = {redis_url}")

