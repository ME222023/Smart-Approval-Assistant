# 这是一个与小智助手关联的应用。
    通过企业微信平台回复用户在小智助手的提问。

### 部署环境
    10.5.5.73
### 部署方式
    # 生成wei_chat镜像
    docker build -t wei_chat:v1  .
    # 使用docker-compose部署
    docker-compose up -d
### 调用接口
    请查看prac.py文件

## 主要介绍两个文件：
### web_api.py : 用于即时回复用户的问题。
    ps： 需要部署到10.5.5.73，才可以联接测试环境的小智助手
    '''
        # 启动脚本 
        python web_api.py
    '''

### send_app.py: 包含创建群聊；上传文件等功能
    ps: 在办公环境即可使用
    