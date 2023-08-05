import redis
from hashids import Hashids

from addok.config import config


hashids = Hashids()


class RedisProxy:
    instance = None
    Error = redis.RedisError

    def connect(self, *args, **kwargs):
        self.instance = redis.StrictRedis(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def next_id(self):
        next_id = self.incr('_id_sequence')
        return hashids.encode(next_id)


DB = RedisProxy()


@config.on_load
def connect():
    params = config.REDIS.copy()
    params.update(config.REDIS.get('indexes', {}))
    DB.connect(
        host=params['host'],
        port=params['port'],
        db=params['db'],
        password=params.get('password')
    )
