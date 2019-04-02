import sys

from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.options import options

from django_env import *  # 加载 Django 环境
from config import CONFIG
from handler import ChatHandler
from log import logger


def main():
    handlers = [('/chatsocket', ChatHandler)]
    chat_app = Application(handlers, **CONFIG)
    chat_app.listen(options.port)
    ChatHandler.globle_listen()

    try:
        ioloop = IOLoop.current()
        ioloop.start()
    except KeyboardInterrupt:
        logger.info('Exit')
        sys.exit(0)


if __name__ == "__main__":
    main()
