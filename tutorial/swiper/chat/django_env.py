'''
加载 Django 环境

直接在需要的地方 `from django_env import *` 即可
'''

import os
import sys

import django

__all__ = ()


CHAT_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(os.path.dirname(CHAT_DIR), 'backend')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiper.settings")
sys.path.insert(0, WEB_DIR)
django.setup()
