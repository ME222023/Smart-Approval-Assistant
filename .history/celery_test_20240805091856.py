from celery_app import add

result = add.delay(4, 6)
print('Task result:', result.get(timeout=10))

result = get_message.delay(user)
print('Message:', result.get(timeout=10))