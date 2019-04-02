import re
import json

PHONENUM_PATTERN = re.compile(r'^1[3-9]\d{9}$')  # 预编译手机号匹配规则


def is_phonenum(phonenum:str):
    '''检查输入的手机号是否正确'''
    phonenum = phonenum.strip()
    if PHONENUM_PATTERN.match(phonenum):
        return True
    else:
        return False


def is_json(test_str):
    '''检查字符串是否是 json'''
    if not isinstance(test_str, (str, bytes)):
        return False

    try:
        json.loads(test_str)
    except (TypeError, JSONDecodeError):
        return False
    else:
        return True
