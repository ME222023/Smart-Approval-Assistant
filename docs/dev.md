# 开发规范
学习之后进行编写
...

# TODO LIST
- [x] 为每个函数添加相应注释，删除不需要的代码和文件夹
- [ ] 配置文件整理 config（chat里面写死的变量都需要配置一遍，不可写死，一定要导入使用）
+ 添加的依赖（新装的库）——> 全白的环境应该如何配置才可运行代码

- [ ] 用户和管理员使用流程的说明和截图（编写display.md和images文件夹）
- [ ] 架构图的学习和绘制（yEd）
- [ ] 制作文件结构图
- [ ] 制作流程图（以上含可以参考千问官方文档）
- [ ] WXBizMsgCrypt3.py
- [ ] chat中部分函数没有用到,是否要全部删除，不删的话是否要按照标准添加函数参数类型和返回值类型

-----------------最最最重要（要设计得当）---------------------------
文件结构说明（tree指令）
存在的没有涉及到的文件不要提及
涉及到的文件需要提
后面直接加上注释
描述package的作用和文件的基本功能
```shell
├── redis_handler 
│   ├── redis_handle.py # RedisClient类
│   └── redis_task_utils.py # redis消息队列相关工具函数集合
├── rule_handler
│   ├── __init__.py
│   ├── rules.py # 规则检测集合
│   └── schema.py # 调度信息参数列表
├── scheduler
│   ├── __init__.py
│   └── schedule_handle.py # 处理调度信息工具函数集合
├── server_logs # wechat_server日志信息
│   ├── server.log
├── utils
│   ├── __init__.py
│   ├── config.py # Config类
│   ├── exception_handle.py # 自定义异常类
│   ├── log_handle.py # server_log函数
├── chat
│   ├── chat_tool.py 
│   ├── ierror.py
│   ├── message_hander.py
│   ├── wechat_client.py
│   └── WXBizMsgCrypt3.py
├── docs
│   ├── dev.md # 开发者文档
│   ├── display.md # 功能展示
│   └── images # 原始图片
├── interaction_handler
│   ├── __init__.py 
│   ├── admin_interact_handle.py # 管理员和小智交互逻辑集合
│   ├── cus_interact_handle.py # 用户和小智交互逻辑集合
├── LLM
│   ├── __init__.py
│   ├── assistant.py # 大模型流程的api调用
├── logs
│   ├── weichat.log # web_api.py的日志信息
├── msg_handler.py # 流程总控程序
├── config.ini # 配置文件
├── web_api.py # 服务器程序
├── requirements.txt # 依赖说明文档
├── README.md # 项目介绍文档
```

# 函数调用图
![](images/schedule_graph.png)
利用drawio绘制
函数模块之间的调用关系（参考动态生成的模块）
但是线路只需要绘制一次且不需要设计公共库

# 架构图
利用drawio绘制
将之前的思路抽象成相应的模块再进行绘制
参考 https://blog.csdn.net/kion0929/article/details/102667123

# 部署
环境准备，依赖安装说明，怎么运行等等
大致的流程（主要分为两个模块即用户和管理员的相关交互）
每个模块用

# 补充requirements.txt
搜索后+相关的依赖

再问一下是否需要绘制用户和管理员与小智交互的流程图

# 测试问题
用户端问题
1. input:请帮我审批zhangxs1名下任务
   output:登录失败，已通知管理员进行处理。
2. input:请帮zhangxs1名下任务
   output:请帮zhangxs1名下任务