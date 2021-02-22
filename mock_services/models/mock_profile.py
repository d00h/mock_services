from abc import ABC, abstractmethod
from typing import Union
import json
from flask import Response as FlaskResponse
from redis import Redis

from .fake_response import FakeResponseCollection


class MockProfile(ABC):

    def __init__(self, name: str):
        self.profile = name

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
    def next_response(self, endpoint, **kwarg) -> FlaskResponse:
        pass


class RedisMockProfile(MockProfile):

    redis: Redis

    def __init__(self,  name: str, redis: Redis, expire=30*60):
        MockProfile.__init__(self, name)
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
        if responses is None or isinstance(responses, list):
            responses = FakeResponseCollection(responses)
        config_data = json.dumps(responses.to_data())
        self.redis.setex(config_key, self.expire, config_data)
        self.reset()

    def reset(self):
        count_key = self._get_count_key('*')
        for key in self.redis.keys(count_key):
            self.redis.delete(key)

    def next_response(self, endpoint, **kwarg) -> FlaskResponse:
        endpoint_responses = self.config.filter_by_endpoint(endpoint)
        max_step = endpoint_responses.max_step

        count_key = self._get_count_key(endpoint)
        count = self.redis.incr(count_key)
        if count == 1:
            self.redis.expire(count_key, self.expire)
        step = (count-1) % (max_step + 1)

        return endpoint_responses.filter_by_step(step).choice()

    def _get_config_key(self) -> str:
        return f'{self.profile}/config'

    def _get_count_key(self, endpoint) -> str:
        return f'{self.profile}/count/{endpoint}'


# class MockService(ABC):

#     @abstractmethod
#     def __getitem__(self, profile_name) -> MockProfile:
#         pass
