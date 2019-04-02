from common.errors import PermissionDenied


def need_perm(perm_name):
    '''Vip 权限检查装饰器'''
    def check(view_function):
        def wrapper(request):
            user = request.user
            if user.vip.has_perm(perm_name):
                return view_function(request)
            else:
                raise PermissionDenied
        return wrapper
    return check
