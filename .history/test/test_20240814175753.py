import configparser

config = configparser.ConfigParser()

config.read("../config.ini")

print(config.get("server", "redis_url"))