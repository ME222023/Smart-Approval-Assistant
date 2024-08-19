from celery_app import *

# result = add.delay(4, 6)
# print('Task result:', result.get(timeout=10))

user = "msg_17a755177f4ad1f1d99bf8042cfbb74a"
result = get_message.delay(user)
print('Message:', result.get(timeout=10))