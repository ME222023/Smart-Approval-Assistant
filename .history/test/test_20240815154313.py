# import configparser

# config = configparser.ConfigParser()

# config.read("/home/hezp1/AI/app_weichat/config.ini")

# print(config.sections())
# print(config.get("server", "admin_list"))

import sys
sys.path.append("/home/hezp1/AI/app_weichat")

from utils.config import Config

config = Config()
config.init("/home/hezp1/AI/app_weichat/config.ini")

redis = config.config['server']['redis_url']
config.token = config.config['DEFAULT']['token']
config.admin_list = config.config['DEFAULT']['admin_list'].split(',')
print(redis)