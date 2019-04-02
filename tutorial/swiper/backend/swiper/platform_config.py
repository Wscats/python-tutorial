'''各个第三方平台的接入配置'''

# 互亿无限短信配置
HY_SMS_URL = 'http://106.ihuyi.com/webservice/sms.php?method=Submit'
HY_SMS_PARAMS = {
    'account': 'C42331298',
    'password': '2d2284b74dc4972da3df3915fb17b28f',
    'content': '您的验证码是：%s。请不要把验证码泄露给其他人。',
    'mobile': None,
    'format': 'json'
}


# 七牛云账号配置
QN_ACCESS_KEY = 'kEM0sRR-meB92XU43_a6xZqhiyyTuu5yreGCbFtw'
QN_SECRET_KEY = 'QxTKqgnOb_UVldphU261qu9IdzmjkgGHh6GQVPPy'
QN_BASE_URL = 'http://ph3wmx4s2.bkt.clouddn.com'
QN_BUCKET = 'swiper'


# 微博 OAuth 认证配置
WB_APP_KEY = '415847342'
WB_APP_SECRET = '25bb6f5efd2f2d69177095562f031e3b'
WB_CALLBACK = 'http://swiper.seamile.org/weibo/callback/'

# 微博授权认证接口
WB_AUTH_API = 'https://api.weibo.com/oauth2/authorize'
WB_AUTH_ARGS = {
    'client_id': WB_APP_KEY,
    'redirect_uri': WB_CALLBACK,
}

# 获取微博令牌接口
WB_ACCESS_TOKEN_API = 'https://api.weibo.com/oauth2/access_token'
WB_ACCESS_TOKEN_ARGS = {
    'client_id': WB_APP_KEY,
    'client_secret': WB_APP_SECRET,
    'grant_type': 'authorization_code',
    'redirect_uri': WB_CALLBACK,
    'code': None,
}

# 获取微博用户数据接口
WB_USER_SHOW_API = 'https://api.weibo.com/2/users/show.json'
WB_USER_SHOW_ARGS = {
    'access_token': None,
    'uid': None,
}
