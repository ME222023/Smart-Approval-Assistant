import configparser

class Config():
    redis_url = None
    token = None
    admin_ids = None
    base_url = None

    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
    
    def init(self, path: str):
        self.config.read(path)