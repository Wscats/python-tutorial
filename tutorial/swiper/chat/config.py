"""系统配置"""
from tornado.options import define

define("port", default="8080", type=int, help="端口号")
define("log_level", default="debug", help="日志等级, 可选项: debug|info|warn|error")
define("log_path", default="chat.log", help="日志路径")
define("log_backup", default=30, type=int, help="日志文件数量")

CONFIG = {
    'cookie_secret': '\x1az\x11tB4\x17g7[Fry)R\xa1a&"\x7f\x1a/r<\x13,:y\xaeR6M',
    'xsrf_cookies': True,
    'autoreload': True,
    'debug': False,
}
