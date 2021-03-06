from copy import deepcopy
import json
import os

import redis

from .initial import initial_data
from web.utils import notify_ui


SESSION_EXPIRE_TIME = 60 * 60 * 24  # 1 day
r = redis.Redis(host=os.environ.get('REDIS_HOST', '127.0.0.1'))


class RedisManager(object):
    '''
    State key/value store base class for the global and session state. Backed by
    Redis. All getting and setting should happen via this class. Keys must be
    defined in initial.py before use. A value can be any type that is JSON
    serializable.
    '''

    def __init__(self):
        self._redis_prefix = 'photomanager:{}:'.format(self._type)
        super().__init__()

    def _redis_key(self, key, channel_name=None):
        if channel_name:
            return '{}:{}:{}'.format(self._redis_prefix, channel_name, key)
        else:
            return '{}:{}'.format(self._redis_prefix, key)

    def get(self, key, channel_name=None, default=None):
        if key not in initial_data[self._type]:
            raise KeyError('Key \'{}\' not in \'{}\''.format(key, self._type))
        val = r.get(self._redis_key(key, channel_name))

        if val:
            val = json.loads(val)
        else:
            val = deepcopy(initial_data[self._type][key])
        return val

    def set(self, key, val, channel_name=None):
        if key not in initial_data[self._type]:
            raise KeyError('Key \'{}\' not in \'{}\''.format(key, self._type))
        val = json.dumps(val)
        if channel_name:
            r.set(self._redis_key(key, channel_name), val, ex=SESSION_EXPIRE_TIME)
            notify_ui(self._type, {key: val}, channel_name)
        else:
            r.set(self._redis_key(key, channel_name), val)
            notify_ui(self._type, {key: val})
        return True

    def increment(self, key, channel_name=None):
        if key not in initial_data[self._type]:
            raise KeyError('Key \'{}\' not in \'{}\''.format(key, self._type))
        val = r.incr(self._redis_key(key, channel_name))
        notify_ui(self._type, {key: val})
        return val

    def decrement(self, key, channel_name=None):
        if key not in initial_data[self._type]:
            raise KeyError('Key \'{}\' not in \'{}\''.format(key, self._type))
        val = r.decr(self._redis_key(key, channel_name))
        notify_ui(self._type, {key: val})
        return val

    def push(self, key, val):
        raise NotImplementedError()

    def pop(self, key):
        raise NotImplementedError()

    def get_all(self, channel_name=None):
        data = {}
        for key in initial_data[self._type].keys():
            data[key] = self.get(key, channel_name)
        return data

    def clear(self, key=None, channel_name=None):
        if not key:
            key = self._type

        if key == 'synchronizer_state':
            print(key)
            # import pdb; pdb.set_trace()
        r.delete(self._redis_key(key, channel_name))

    def clear_all(self, channel_name=None):
        for key in initial_data[self._type]:
            self.clear(key, channel_name)

    def delete_obsolete(self):
        raise NotImplementedError()
