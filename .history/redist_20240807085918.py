import redis

redis_url = "redis://:123@10.5.5.73:16379/0"
# redis_url = "redis://:123@10.5.5.73:16379/1"
r = redis.from_url(redis_url)

# 定义要操作的队列名称
queue_name = 'my_queue'

# 向队列中推送元素
def push_to_queue(element):
    r.lpush(queue_name, element)
    print(f"Pushed {element} to queue")

# 从队列中弹出元素
def pop_from_queue():
    element = r.rpop(queue_name)
    if element:
        print(f"Popped {element.decode('utf-8')} from queue")
    else:
        print("Queue is empty")

# 打印队列中的所有元素
def print_all_elements():
    elements = r.lrange(queue_name, 0, -1)  # 获取列表中所有元素
    if elements:
        print("All elements in the queue:")
        for element in elements:
            print(element.decode('utf-8'))
    else:
        print("Queue is empty")
