from .config import Config
if not Config.redis_url:
    Config("config.ini", "oa.csv")
