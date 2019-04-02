import random

import requests

from swiper import platform_config
from worker import call_by_worker


def gen_verify_code(length=4):
    '''生成验证码'''
    if length <= 0:
        length = 1
    code = random.randrange(10 ** (length - 1), 10 ** (length))
    return str(code)


def send_sms(phone_num, text):
    '''发送短信'''
    params = platform_config.HY_SMS_PARAMS.copy()
    params['mobile'] = phone_num
    params['content'] = params['content'] % text
    headers = {
        "Accept": "text/plain",
        "Content-type": "application/x-www-form-urlencoded"
    }
    response = requests.post(platform_config.HY_SMS_URL, data=params, headers=headers)
    return response


async_send_sms = call_by_worker(send_sms)  # 为方便调试，将异步调用单独定义一次
