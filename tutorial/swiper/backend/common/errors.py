# coding: utf-8
'''
程序内部错误

程序内部正常的逻辑错误直接抛出异常给前端，经过异常中间件的时候会将对应的错误码返回给前端
'''


class LogicError(Exception):
    '''程序内部逻辑错误'''
    code = None
    data = None

    def __init__(self, data=None):
        self.data = data  # 发生异常时需要传回前端的数据

    def __str__(self):
        return self.__class__.__name__

    @property
    def msg(self):
        return self.data or self.__class__.__name__


def gen_error(name: str, err_code: int) -> LogicError:
    base_cls = (LogicError,)
    cls_attr = {'code': err_code}
    return type(name, base_cls, cls_attr)


# 正常
OK = gen_error('OK', 0)

# 通用错误
InternalError = gen_error('InternalError', 500)         # 服务器内部错误
ParamsError = gen_error('ParamsError', 1001)            # 参数错误
DataError = gen_error('DataError', 1002)                # 数据错误
DoseNotExist = gen_error('DoseNotExist', 1003)          # 不存在
ReachUpperLimit = gen_error('ReachUpperLimit', 1004)    # 达到上限
PermissionDenied = gen_error('PermissionDenied', 1005)  # 没有权限
Timeout = gen_error('Timeout', 1006)                    # 超时
Expired = gen_error('Expired', 1007)                    # 已过期
NotYetTime = gen_error('NotYetTime', 1008)              # 时间未到
InvalidPhone = gen_error('InvalidPhone', 1009)          # 无效手机号
InvalidPIN = gen_error('InvalidPIN', 1010)              # 无效验证码

# 用户类错误
LoginRequired = gen_error('LoginRequired', 2000)    # 用户未登录
NameConflict = gen_error('NameConflict', 2001)      # 名字冲突
MoneyNotEnough = gen_error('MoneyNotEnough', 2002)  # 金钱不足
UserNotExist = gen_error('UserNotExist', 2003)      # 用户不存在
NotYourFriend = gen_error('NotYourFriend', 2004)    # 不是好友关系

# 第三方错误
WeiboAccessTokenError = gen_error('WeiboAccessTokenError', 9000) # AccessToken 接口错误
WeiboUserShowError = gen_error('WeiboUserShowError', 9000)       # UserShow 接口错误
