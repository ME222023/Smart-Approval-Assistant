import redis
import logging

logger = logging.getLogger("server_log")


class RedisClient:
    """
    RedisClient类用于管理Redis连接，提供一个上下文管理器接口来简化连接的打开和关闭操作。
    详细描述：
    该类使用上下文管理器协议（__enter__ 和 __exit__ 方法）来确保连接在使用后自动关闭。
    通过传入Redis的URL来初始化连接，方便在不同环境下使用。
    """

    def __init__(self, redis_url: str):
        """
        初始化RedisClient实例并建立到Redis服务器的连接。
        @param redis_url: Redis服务器的URL
        """
        self.client = redis.Redis.from_url(redis_url)

    def __enter__(self):
        """
        进入上下文管理器时调用，返回Redis客户端实例。
        """
        return self.client
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        退出上下文管理器时调用，关闭Redis连接并处理异常。
        @param exc_type: Exception type, 异常类型
        @param exc_value: Exception value, 异常值
        @param traceback: Traceback, 异常追踪信息
        @return: bool, 返回False以便将异常继续传播
        """
        self.client.close()
        if exc_type is not None:
            logger.debug(f"An exception of type {exc_type} occurred with value {exc_value}")
        return False
