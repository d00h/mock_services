import json
from abc import ABC, abstractmethod
from typing import Union

from redis import Redis

from .fake_response import FakeResponseCollection, FakeResponse


class MockProfile(ABC):

    @property
    @abstractmethod
    def config(self) -> FakeResponseCollection:
        pass

    @config.setter
    @abstractmethod
    def config(self, responses: Union[FakeResponseCollection, list]):
        pass

    @abstractmethod
    def reset(self):
        """ drop state of profile counts """

    @abstractmethod
    def next_response(self, endpoint) -> FakeResponse:
        pass

    @staticmethod
    def create(redis: Redis, expire) -> 'MockProfile':
        return RedisMockProfile(redis, expire)


class RedisMockProfile(MockProfile):

    redis: Redis

    def __init__(self,  redis: Redis, expire=30*60):
        self.redis = redis
        self.expire = expire

    @property
    def config(self) -> FakeResponseCollection:
        config_key = self._get_config_key()
        config_data = self.redis.get(config_key)
        if config_data is None:
            return FakeResponseCollection()
        data = json.loads(config_data)
        return FakeResponseCollection.from_list(data)

    @config.setter
    def config(self, responses: Union[FakeResponseCollection, list]):
        config_key = self._get_config_key()
        if responses is None:
            responses = FakeResponseCollection()
        if isinstance(responses, list):
            responses = FakeResponseCollection.from_list(responses)
        config_data = json.dumps(responses.to_data())
        self.redis.setex(config_key, self.expire, config_data)
        self.reset()

    def reset(self):
        count_key = self._get_count_key('*')
        for key in self.redis.keys(count_key):
            self.redis.delete(key)

    def next_response(self, endpoint) -> FakeResponse:
        endpoint_responses = self.config.filter_by_endpoint(endpoint)
        max_step = endpoint_responses.max_step

        count_key = self._get_count_key(endpoint)
        count = self.redis.incr(count_key)
        if count == 1:
            self.redis.expire(count_key, self.expire)
        step = (count-1) % (max_step + 1)

        return endpoint_responses.filter_by_step(step).choice()

    def _get_config_key(self) -> str:
        return 'config'

    def _get_count_key(self, endpoint) -> str:
        return f'count/{endpoint}'
