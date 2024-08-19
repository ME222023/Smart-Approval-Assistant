from interact.test import add

result = add.delay(4, 6)
print('Task result:', result.get(timeout=10))

# get_message()
# print_ok_approval()
# print_wait_approval()
# addMsg()
# printMsg()