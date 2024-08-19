import configparser

config = configparser.ConfigParser()

config.read("../config.ini")

print(config.sections())
print(config.get("server", "redis_url"))