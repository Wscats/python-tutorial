# -*- coding: utf-8 -*-

import time
from redis import Redis as _Redis
from redis.client import BasePipeline
from pickle import dumps, loads, UnpicklingError

from django.conf import settings


class Redis(_Redis):
    '''
    Redis继承类

    接口与原生 Redis 保持一致，增加自动序列化、反序列化功能
    '''
    def __init__(self, *args, **kwargs):
        _Redis.__init__(self, *args, **kwargs)

    def keys(self, pattern='*'):
        'Returns a list of keys matching ``pattern``'
        return sorted(_Redis.keys(self, pattern))

    def set(self, key, value, timeout=0):
        if timeout > 0:
            return self.setex(key, dumps(value, 1), timeout)
        else:
            return _Redis.set(self, key, dumps(value, 1))

    def setnx(self, key, value, timeout=0):
        res = _Redis.setnx(self, key, dumps(value, 1))
        if res and timeout > 0:
            _Redis.expire(self, key, timeout)
        return res

    def get(self, key, default=None):
        value = _Redis.get(self, key)
        return default if value is None else value

    def mset(self, mapping):
        return _Redis.mset(self, {k: dumps(v, 1) for k, v in mapping.items()})

    def mget(self, keys, default=None):
        values = _Redis.mget(self, keys)
        return [default if v is None else v for v in values]

    def hset(self, name, key, value):
        return _Redis.hset(self, name, key, dumps(value, 1))

    def hget(self, name, key, default=None):
        value = _Redis.hget(self, name, key)
        return default if value is None else value

    def hmset(self, name, mapping):
        return _Redis.hmset(self, name, {k: dumps(v, 1) for k, v in mapping.items()})

    def hmget(self, name, keys, default=None):
        values = _Redis.hmget(self, name, keys)
        return [default if v is None else v for v in values]

    def pop(self, key, default=None):
        '''del specified key and return the corresponding value'''
        pipe = self.pipeline()
        pipe.get(key)
        pipe.delete(key)
        value, res = pipe.execute()
        return default if value is None or res != 1 else value

    def hpop(self, name, key, default=None):
        '''del specified key and return the value of key within the hash name'''
        pipe = self.pipeline()
        pipe.hget(name, key)
        pipe.hdel(name, key)
        value, res = pipe.execute()
        return default if value is None or res != 1 else value

    def hscan_iter(self, name, match=None, count=None):
        cursor = '0'
        found = []
        while cursor != 0:
            cursor, data = self.hscan(name, cursor=cursor,
                                      match=match, count=count)
            for k, v in data.items():
                if k not in found:
                    found.append(k)
                    yield k, v

    def unpickle(self, data):
        try:
            if isinstance(data, bytes):
                return loads(data)
            elif isinstance(data, (list, tuple)):
                return [self.unpickle(v) for v in data]
            elif isinstance(data, dict):
                return {k: self.unpickle(v) for k, v in data.items()}
            else:
                return data
        except (UnpicklingError, TypeError, ValueError, EOFError):
            return data

    def parse_response(self, connection, command_name, **options):
        '''Parses a response from the Redis server'''
        response = _Redis.parse_response(self, connection, command_name, **options)
        return self.unpickle(response)

    def pipeline(self, transaction=True, shard_hint=None, origin=False):
        if origin:
            return _Redis.pipeline(self, transaction, shard_hint)
        else:
            return Pipeline(self.connection_pool, self.response_callbacks,
                            transaction, shard_hint)


class Pipeline(BasePipeline, Redis):
    '''覆盖原生Pipeline类'''
    def execute(self, raise_on_error=True):
        result = super(Pipeline, self).execute(raise_on_error)
        return [self.unpickle(r) for r in result]


class MSRedis(object):
    '''读写分离客户端 (只针对程序中用到的命令)'''
    def __init__(self, conf):
        self.master = Redis(**conf['Master'])
        self.slave = Redis(**conf['Slave'])
        self.read_commands = [
            'ttl', 'exists', 'expire', 'get', 'keys',
            'hget', 'hgetall', 'hkeys', 'hmget',
            'sismember', 'smembers', 'sdiff', 'sinter', 'sunion'
            'zrevrange', 'zrevrangebyscore', 'zrevrank', 'zscore'
        ]

    def __getattribute__(self, name):
        if name in ['master', 'slave', 'read_commands']:
            return object.__getattribute__(self, name)
        elif name in self.read_commands:
            return self.slave.__getattribute__(name)
        else:
            return self.master.__getattribute__(name)


# 创建全局 Redis 连接
rds = MSRedis(settings.REDIS)
