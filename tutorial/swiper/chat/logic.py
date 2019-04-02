import json
from importlib import import_module

from django.conf import settings


def get_web_session(session_key):
    '''获取 Web 端的 session'''
    engine = import_module(settings.SESSION_ENGINE)
    session = engine.SessionStore(session_key)
    return session


def pack_msg(packet):
    msg = json.dumps(packet, ensure_ascii=False, separators=(',', ':'))
    return msg.encode('utf8')
