import configparser

config = configparser.ConfigParser()

config.read("/home/hezp1/AI/app_weichat/config.ini")

print(config.sections())
print(config.get("server", "redis_url"))