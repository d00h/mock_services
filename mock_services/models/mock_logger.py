from abc import ABC, abstractmethod
from redis import Redis


class MockLogger(ABC):

    def __init__(self, name: str):
        self.profile = name

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def add(self, endpoint, **kwargs):
        pass


class RedisMockLogger(MockLogger):

    def __init__(self, name, redis: Redis, expire: int):
        MockLogger.__init__(self, name)
        self.redis = redis
        self.expire = expire

    def clear(self):
        pass

    def add(self, endpoint, **kwargs):
        pass
