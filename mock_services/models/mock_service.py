from typing import Iterable

from redis import Redis

from .mock_logger import MockLogger, RedisMockLogger
from .mock_profile import MockProfile, RedisMockProfile


class MockService(object):

    def __init__(self, redis: Redis, expire):
        self.redis = redis
        self.expire = expire

    def get_profile(self, profile_name: str) -> MockProfile:
        return RedisMockProfile(profile_name, self.redis, self.expire)

    def get_logger(self, profile_name: str) -> MockLogger:
        return RedisMockLogger(profile_name, self.redis, self.expire)

    def find_profiles(self, prefix=None) -> Iterable[str]:
        result = set()
        pattern = '{0}*'.format(prefix or '')
        for key in self.redis.keys(pattern):
            name, _ = key.decode().split('/', maxsplit=1)
            result.add(name)
        return list(result)
