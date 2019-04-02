import time
from json import dumps, loads
from collections import namedtuple, defaultdict

from tornadoredis import Client
from tornado.gen import coroutine, Task
from tornado.websocket import WebSocketHandler

# 从 Web 端引入
from django.conf import settings
from lib.cache import rds
from user.models import User

# 从 Chat 本身引入
import log
import logic

Packet = namedtuple('Packet', ['tag', 'data'])


class ChatHandler(WebSocketHandler):
    '''WebSocket 处理类
        1. 客户端需要先登陆 Web 系统，取得 session id 再来与 Chat Server 建立连接
        2. 连接时 header 中传入用户唯一标识 session_id

        数据结构
            connections: {
                uid1: conn_user_1,
                uid2: conn_user_2,
            }

        频道格式: "频道名" 或 "频道名:其他标识"
            BROADCAST
            PRIVATE:uid
    '''
    connections = {}

    def __init__(self, application, request, **kwargs):
        super().__init__(self, application, request, **kwargs)
        self.uid = None
        self.user = None
        self.sessionid = None
        self.rds = None

    def get_compression_options(self):
        '''启用压缩'''
        return {}

    def get_current_user(self):
        '''当前用户'''
        return self.user

    def send_to_client(self, tag, data):
        '''打包数据, 并发送给客户端'''
        packet = Packet(tag, data)
        message = logic.pack_msg(packet)
        self.write_message(message)

    @staticmethod
    def connect_redis():
        rds = Client(host=settings.REDIS['Master']['host'],
                     port=settings.REDIS['Master']['port'],
                     selected_db=settings.REDIS['Master']['db'])
        rds.connect()
        return rds

    @classmethod
    def kick_out(cls, uid):
        '''强制踢下线'''
        old_conn = cls.connections.pop(uid)
        old_conn.close(499, 'KickOut')
        log.logger.error('KickOut: ip=%s id=%s' % (old_conn.request.remote_ip, uid))
        del old_conn

    def open(self):
        '''WebSocket连接完成后的处理'''
        # 检查客户端是否已登陆 Web 系统
        session_name = settings.SESSION_COOKIE_NAME
        sessionid = self.request.headers.get(session_name)
        session = logic.get_web_session(sessionid)
        if sessionid is None or not session.has_key(session_name):
            self.close(403, 'Forbidden')
            log.logger.error('Connection refused: %s' % self.request.remote_ip)
            return

        try:
            # 检查重复登录, 新的登陆会把旧的顶下去
            if uid in ChatHandler.connections:
                self.kick_out(uid)

            # 保存 connections
            self.uid = uid
            self.user = User.get(uid=session['uid'])
            self.sessionid = sessionid
            self.login_time = int(time.time())
            self.rds = self.connect_redis()  # 异步redis连接 (用于监听用户相关消息)
            ChatHandler.connections[self.uid] = self

            self.pull_history_chat()  # 拉取历史消息并回写给 client
            self.listen()
        except Exception:
            log.trace_err()

    @coroutine
    def listen(self):
        '''监听用户频道'''
        def handle_private_msg(msg):
            '''处理私人消息'''
            try:
                log.logger.debug('Receive user msg: %s' % repr(msg))
                if msg.kind == 'message' and msg.channel.startswith('PRIVATE:'):
                    self.write_message(msg.body)
            except Exception:
                log.trace_err()

        try:
            # 添加订阅
            channels = ['PRIVATE:%s' % self.uid]  # 私聊
            yield Task(self.rds.subscribe, channels)
            self.rds.listen(handle_private_msg)
        except Exception:
            log.trace_err()

    @classmethod
    @coroutine
    def globle_listen(cls):
        '''
        监听全局频道

        全局广播频道使用单独的监听器, 收到消息后直接写回客户端
        '''
        def handle_global_msg(msg):
            '''处理全局消息'''
            try:
                log.logger.debug('Receive globle msg: %s' % repr(msg))
                if msg.kind == 'message':
                    # 向所有客户端推送消息
                    for cli_conn in cls.connections.values():
                        cli_conn.write_message(msg.body)
            except Exception:
                log.trace_err()

        try:
            # 检查全局监听器
            rds_listener = cls.connect_redis()

            # 开启 PUB/SUB 监听
            channels = ['BROADCAST']
            yield Task(rds_listener.subscribe, channels)
            rds_listener.listen(handle_global_msg)
        except Exception:
            log.trace_err()

    def on_message(self, message):
        '''处理客户端发来的消息'''
        try:
            log.logger.debug('Get request: %s' % repr(message))
            packet = Packet(*loads(message))
        except (TypeError, ValueError) as e:
            self.send_to_client('ERR', 'DataError')
            return

        try:
            if packet.tag == 'PRIVATE':
                # 将私聊消息发给目标用户
                self.private_chat(packet.data['to'], packet.data['msg'])

            elif packet.tag == 'BROADCAST':
                # 发送广播
                self.broadcast(packet.data)

            else:
                # 无法匹配类型
                log.logger.error('Can not match the msg: %s' % repr(message))
        except Exception:
            log.trace_err()

    @coroutine
    def pull_history_chat(self):
        '''拉取历史聊天记录'''
        try:
            # 获取 redis 缓存的消息
            with self.rds.pipeline() as pipe:
                p_channel = 'PRIVATE:%s' % self.uid
                pipe.lrange(p_channel, 0, -1)
                pipe.delete(p_channel)
                res = yield Task(pipe.execute)

            p_chats = [loads(chat)[1] for chat in res[0]]
            self.send_to_client('HISTORY', p_chats)
        except Exception:
            log.trace_err()

    def pack_chat_msg(self, channel, msg):
        '''封装私聊消息'''
        data = {
            'tm': int(time.time()),          # 时间戳
            'from': self.uid,                # 发送者 uid
            'nickname': self.user.nickname,  # 昵称
            'avatar': self.user.avatar[0],   # 头像 ID
            'msg': msg,                      # 消息内容
        }
        packet = Packet(channel, data)
        return logic.pack_msg(packet)

    def private_chat(self, to_uid, msg):
        '''私人聊天'''
        channel = 'PRIVATE:%s' % to_uid
        message = self.pack_chat_msg('PRIVATE', msg)

        if rds.hexists(ckeys.AUTH_TKIDX, to_uid):
            rds.publish(channel, message)
        else:
            log.logger.debug('Publish pchat to LIST: %s' % repr(message))
            rds.rpush(channel, message)

    def broadcast(self, msg):
        '''广播'''
        packet = Packet('BROADCAST', msg)
        message = logic.pack_msg(packet)
        rds.publish('BROADCAST', message)

    def on_close(self):
        try:
            # 取消订阅
            if getattr(self, 'rds', None) and self.rds.subscribed:
                self.rds.unsubscribe(self.rds.subscribed)
                self.rds.disconnect()

            if hasattr(self, 'uid'):
                # 清理 WebSocket connections
                ChatHandler.connections[self.server].pop(self.uid, None)
        except Exception as e:
            log.trace_err()
