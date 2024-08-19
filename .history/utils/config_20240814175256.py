import configparser

class Config():
    redis_url = ""
    token = ""
    admin_list = []

    def __init__(self) -> None:
        pass
    
    def init(self, ):
        conf_path = "import configparser"