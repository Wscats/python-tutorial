import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiper.settings')

# TODO
#   异步上传头像到七牛云
#   异步登录后自动加载数据到 redis
#   异步存储处理

# 创建 Celery Application
celery_app = Celery('swiper')
celery_app.config_from_object('worker.config')
celery_app.autodiscover_tasks()


def call_by_worker(func):
    '''将任务在 Celery 中异步执行'''
    task = celery_app.task(func)
    return task.delay
