from urllib.parse import urlencode

from swiper import platform_config
from lib.cache import rds
from lib.http import require_post, render_json
from common import errors
from common import keys
from common.utils import is_phonenum
from user.models import User
from user.forms import ProfileForm
from user.logic import send_login_code
from user.logic import upload_avatar_to_cloud
from user.logic import get_wb_access_token
from user.logic import wb_user_show


def verify_phone(request):
    '''提交手机号，向用户发送验证码'''
    phone_num = request.GET.get('phone', '')
    if is_phonenum(phone_num):
        send_login_code(phone_num)
        return render_json()
    else:
        raise errors.InvalidPhone


@require_post
def login(request):
    '''提交验证码并登录'''
    phone_num = request.POST.get('phone')
    code = request.POST.get('code')
    key = keys.LOGIN_SMS_KEY % phone_num
    if rds.get(key) != code:
        raise errors.InvalidPIN

    # 获取用户，并执行登陆操作
    user, created = User.get_or_create(phonenum=phone_num)
    if created:
        user.init()
    request.session['uid'] = user.id
    return render_json({'user': user.to_dict()})


def show_profile(request):
    '''查看配置'''
    result = request.user.profile.to_dict()
    return render_json(result)


@require_post
def update_profile(request):
    '''修改用户配置'''
    profile = request.user.profile
    form = ProfileForm(request.POST, instance=profile)
    if form.is_valid():
        form.save()
        return render_json()
    else:
        raise errors.ParamsError


@require_post
def upload_avatar(request):
    '''上传头像'''
    avatar = request.user.avatar
    upload_avatar_to_cloud(avatar, request.POST)
    return render_json()


def weibo_authurl(request):
    auth_url = '%s?%s' % (platform_config.WB_AUTH_API, urlencode(platform_config.WB_AUTH_ARGS))
    return render_json({'auth_url': auth_url})


def weibo_callback(request):
    '''微博回调接口'''
    code = request.GET.get('code')

    # 获取 access_token
    access_token, wb_uid = get_wb_access_token(code)
    if access_token is None:
        raise errors.WeiboAccessTokenError

    # 获取微博的用户数据
    screen_name, avatar = wb_user_show(access_token, wb_uid)
    if screen_name is None:
        raise errors.WeiboUserShowError

    # 利用微博的账号，在论坛内进行登陆、注册
    nickname = '%s_wb' % screen_name
    user, is_created = User.get_or_create(nickname=nickname)
    user.avatar.first = avatar
    user.avatar.save()
    user.save()

    # 记录用户状态
    request.session['uid'] = user.id

    return render_json({'user': user.to_dict()})
