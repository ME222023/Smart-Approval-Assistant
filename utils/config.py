import pandas as pd
import configparser
from pandas import DataFrame
from chat.wechat_client import WechatClient


class Config:
    """
    Config类用于读取和存储配置文件和CSV文件中的配置信息。
    
    详细描述：
    该类通过读取配置文件和CSV文件来初始化各种配置参数，并提供方法来进行配置参数的转换和获取。
    配置参数包括Redis的URL、令牌、管理员名称、管理员ID和基础URL等。
    该类还提供了根据管理员名称获取管理员ID的功能。
    
    属性说明：
    - redis_url: str, Redis服务器的URL
    - token: str, 认证令牌
    - admin_names: str, 管理员名称列表，以'|'分隔
    - admin_ids: str, 管理员ID列表，以'|'分隔
    - base_url: str, 基础URL
    - oa_map: DataFrame, 包含员工信息的DataFrame
    - wechat_client: WechatClient的实例化对象
    """
    # server
    redis_url = None
    token = None
    admin_names = None
    admin_ids = None
    base_url = None
    # oa用户
    oa_map: DataFrame = None
    # client
    wechat_client = WechatClient()
    # LLM
    url = None
    # chat
    sToken = None
    sEncodingAESKey = None
    sReceiveId = None
    AgentId = None
    Secret = None

    def __init__(self, path: str, csv_path: str):
        """
        初始化Config实例，并读取配置文件和CSV文件。
        
        @param path: str, 配置文件的路径
        @param csv_path: str, CSV文件的路径
        @return: None
        """
        self.init(path, csv_path)

    @classmethod
    def init(cls, path: str, csv_path: str):
        """
        读取配置文件和CSV文件，并初始化类属性。
        
        @param path: str, 配置文件的路径
        @param csv_path: str, CSV文件的路径
        """
        config = configparser.ConfigParser()
        config.read(path)
        
        # 配置文件'server' 的部分
        cls.redis_url = config.get('server', 'redis_url')
        cls.token = config.get('server', 'token')
        cls.admin_names = config.get('server', 'admin_names')
        cls.base_url = config.get('server', 'base_url')
        # 配置文件llm部分
        cls.url = config.get('llm', 'url')
        # 配置文件wechat部分
        cls.sToken = config.get('wechat', 'sToken')
        cls.sEncodingAESKey = config.get('wechat', 'sEncodingAESKey')
        cls.sReceiveId = config.get('wechat', 'sReceiveId')
        cls.AgentId = config.get('wechat', 'AgentId')
        cls.Secret = config.get('wechat', 'Secret')
        # 读取 CSV 文件并赋值给 oa_map
        cls.oa_map = pd.read_csv(csv_path)

        # adminName2Id()将admin_names转成admin_ids
        cls.admin_ids = cls.unames_to_uids()

        
    

    @classmethod
    def get_uid_uname(cls, uid: str = None, uname: str = None) -> str:
        """
        根据员工ID或员工名称获取对应的员工名称或员工ID。
        
        @param uid: str, 员工ID（可选）
        @param uname: str, 员工名称（可选）
        @return: str, 对应的员工名称或员工ID
        """
        df = cls.oa_map
        if uid:
            uname = df[df["emp_id"].str.contains(uid)]
            return uname["emp_oa"].values[0]
        if uname:
            u_id = df[df["emp_oa"].str.contains(uname)]
            return u_id["emp_id"].values[0]
        return ""
    
    @classmethod
    def unames_to_uids(cls) -> str:
        """
        将管理员名称列表转换为管理员ID列表。
        
        @return: str, 管理员ID列表，以'|'分隔
        """
        a_names = cls.admin_names.split('|')
        id_list = []
        for a_name in a_names:
            a_id = cls.get_uid_uname(None, a_name)
            id_list.append(a_id)
        return '|'.join(id_list)
