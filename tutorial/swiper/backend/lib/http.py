from json import loads
from json import dumps
from json import JSONDecodeError

from common.errors import OK
from common.errors import LogicError
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed


def render_json(data=None, error=OK) -> HttpResponse:
    '''
    将返回值渲染为 JSON 数据

    Params:
        data: 返回的数据，一般为一个字典类型，确保每个字段的值都可以被序列化
        error: 逻辑错误信息，是 LogicError 的子类或实例
    '''
    if isinstance(error, type) and issubclass(error, LogicError):
        error = error()

    result = {
        'data': data or error.msg,
        'code': error.code  # 状态码
    }

    if settings.DEBUG:
        # Debug 模式时，按规范格式输出 json
        json_str = dumps(result, ensure_ascii=False, indent=4, sort_keys=True)
    else:
        # 正式环境下，将返回数据压缩
        json_str = dumps(result, ensure_ascii=False, separators=[',', ':'])

    return HttpResponse(json_str)


def allow_http_methods(*methods):
    """检查允许的 HTTP 方法"""
    def decor(view_func):
        def wrap(request, *args, **kwargs):
            nonlocal methods
            methods = [m.upper() for m in methods]
            if request.method not in methods:
                return HttpResponseNotAllowed(methods)
            return view_func(request, *args, **kwargs)
        return wrap
    return decor


require_post = allow_http_methods('post')
