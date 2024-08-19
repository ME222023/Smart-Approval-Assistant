from celery_app import *

# result = add.delay(4, 6)
# print('Task result:', result.get(timeout=10))

addMsg()
printMsg()

add_result = addMsg.delay()
    add_result.get()  # 等待任务完成

    # 调用 printMsg 任务
    print_result = printMsg.delay()
    print_result.get()  # 等待任务完成