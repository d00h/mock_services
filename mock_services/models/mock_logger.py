import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable

from redis import Redis


class MockLogger(ABC):

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def add(self, endpoint, **kwargs):
        pass

    @abstractmethod
    def __iter__(self) -> Iterable[dict]:
        pass

    @staticmethod
    def create(redis: Redis, expire) -> 'MockLogger':
        return RedisMockLogger(redis, expire)


LOG_PAGE = 100


class RedisMockLogger(MockLogger):

    def __init__(self, redis: Redis, expire: int):
        self.redis = redis
        self.expire = expire

    def clear(self):
        log_key = self._get_log_key()
        self.redis.delete(log_key)

    def add(self, endpoint, **kwargs):
        log_key = self._get_log_key()
        data = {
            'endpoint': endpoint,
            'time': datetime.utcnow()
        }
        data.update(**kwargs)
        count = self.redis.lpush(
            log_key, json.dumps(data, default=self.serialize))
        if count == 1:
            self.redis.expire(log_key, self.expire)

    def __iter__(self) -> Iterable[dict]:
        log_key = self._get_log_key()
        count = self.redis.llen(log_key)

        for start in range(0, count, LOG_PAGE):
            items = self.redis.lrange(log_key, start, min(start+LOG_PAGE, count))
            for item in items:
                yield json.loads(item)

    def _get_log_key(self) -> str:
        return 'log'

    @classmethod
    def serialize(cls, o):
        if isinstance(o, (datetime)):
            return o.isoformat()
