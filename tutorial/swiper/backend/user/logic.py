import requests

from lib.cache import rds
from lib import sms
from lib.qiniu import qiniu_upload_data
from common import keys
from common import errors
from swiper import platform_config
from worker import call_by_worker


def send_login_code(phone_num):
    '''发送登陆验证短信'''
    key = keys.LOGIN_SMS_KEY % phone_num
    if not rds.exists(key):
        random_code = sms.gen_verify_code(4)
        sms.async_send_sms(phone_num, random_code)
        rds.setex(key, random_code, 180)  # 状态码有效期 180s
    else:
        raise errors.NotYetTime


@call_by_worker
def upload_avatar_to_cloud(avatar, files):
    '''将图片上传至七牛云'''
    for field_name, file_obj in files.items():
        # 上传
        filename = 'avatar-%s-%s' % (avatar.id, field_name)
        qiniu_upload_data(platform_config.QN_BUCKET, file_obj, filename)
        # 设置属性
        url = '%s/%s' % (platform_config.QN_BASE_URL, filename)
        setattr(avatar, field_name, url)
    avatar.save()


def get_wb_access_token(code):
    '''获取微博的 Access Token'''
    # 构造参数
    args = platform_config.WB_ACCESS_TOKEN_ARGS.copy()
    args['code'] = code

    response = requests.post(platform_config.WB_ACCESS_TOKEN_API, data=args)  # 发送请求
    data = response.json()  # 提取数据
    if 'access_token' in data:
        access_token = data['access_token']
        uid = data['uid']
        return access_token, uid
    else:
        return None, None


def wb_user_show(access_token, wb_uid):
    '''根据微博用户ID获取用户信息'''
    # 构造参数
    args = platform_config.WB_USER_SHOW_ARGS
    args['access_token'] = access_token
    args['uid'] = wb_uid

    # 发送请求
    response = requests.get(platform_config.WB_USER_SHOW_API, params=args)
    data = response.json()
    if 'screen_name' in data:
        screen_name = data['screen_name']
        avatar = data['avatar_hd']
        return screen_name, avatar
    else:
        return None, None
