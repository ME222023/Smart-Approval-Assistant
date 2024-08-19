from celery_app import *

# result = add.delay(4, 6)
# print('Task result:', result.get(timeout=10))

print('Message:', result.get(timeout=10))
print(type(result.get(timeout=10)))