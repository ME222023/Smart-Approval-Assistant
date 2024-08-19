from celery import Celery

broker="redis://:123@10.5.5.73:16379/2"
app = Celery('tasks', broker=broker)