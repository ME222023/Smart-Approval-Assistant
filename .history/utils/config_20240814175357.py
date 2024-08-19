import configparser

class Config():
    redis_url = ""
    token = ""
    admin_list = []

    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
    
    def init(self, path: str):
        self.config.read()