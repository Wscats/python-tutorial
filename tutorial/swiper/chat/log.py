import os
import sys
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler

from tornado import log
from tornado.options import options

__all__ = ('logger', 'trace_err')


def configure_loggers():
    # 获取参数
    path = options.log_path
    backup = options.log_backup
    level = getattr(logging, options.log_level.upper())

    # 定义日志格式: '时间 级别 [模块名.函数名 ]: message'
    fmt = ('%(color)s%(asctime)s %(levelname)5.5s '
           '[%(module)s.%(funcName)s]%(end_color)s: %(message)s')
    formatter = log.LogFormatter(datefmt="%Y-%m-%d %H:%M:%S", fmt=fmt)
    log_handler = TimedRotatingFileHandler(path, when='D', backupCount=backup)
    log_handler.setFormatter(formatter)

    # 设置 handler
    for name in ["tornado.application", "tornado.general", "tornado.access"]:
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(log_handler)

configure_loggers()
logger = logging.getLogger("tornado.application")


def trace_err():
    '''
    将捕获到的异常信息输出到错误日志

    直接放到 expect 下即可
    示例:
        try:
            raise ValueError
        except Exception, e:
            trace_err()
    '''
    split_line = lambda title: '\n%s\n' % title.center(50, '-')

    # 取出格式化的异常信息
    msg = split_line(' Error ')
    msg += traceback.format_exc()

    # 取出异常位置的参数
    msg += split_line(' Args ')
    for k, v in sorted(sys._getframe(1).f_locals.items()):
        msg += '>>> %s: %s\n' % (k, v)

    logger.error(msg)
