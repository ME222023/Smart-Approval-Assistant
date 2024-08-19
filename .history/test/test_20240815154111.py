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
redis = config.admin_list
print(redis)