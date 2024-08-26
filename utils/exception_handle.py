class LoginException(Exception):
    """
    LoginException类用于表示登录过程中发生的异常。
    该异常类继承自内置的Exception类，用于在登录失败或发生错误时抛出自定义异常。
    可以通过传递一条消息来描述具体的异常原因。
    """

    def __init__(self, msg: str):
        """
        初始化LoginException实例，并设置异常消息。
        @param msg: s异常消息，描述登录失败的原因
        """
        self.msg = msg
        super().__init__(self.msg)
