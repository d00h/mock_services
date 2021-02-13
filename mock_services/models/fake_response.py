from collections import defaultdict
from dataclasses import dataclass
from os import path
from random import randrange
from typing import DefaultDict, Iterable, List, Optional

import yaml
from faker import Faker
from flask import Response as FlaskResponse
from jinja2 import Template
from werkzeug.exceptions import GatewayTimeout

TEMPLATE_FUNCS = {
    'word': lambda: Faker().word(),
    'address': lambda: Faker().address(),
    'uuid4': lambda: Faker().uuid4(),
    'md5': lambda: Faker().md5(),
    'email': lambda: Faker().email(),
}


@dataclass
class FakeResponse(object):

    endpoint: str

    chance: int = 100
    step: int = 0

    status: int = 200
    body_template: str = None
    headers: dict = None
    mimetype: str = None
    content_type: str = None

    def __post_init__(self):
        if self.step < 0:
            raise ValueError(f'step = {self.step}')
        if self.chance <= 0:
            raise ValueError(f'chance = {self.chance}')

    def __hash__(self):
        return hash(str(self))

    @classmethod
    def json(cls, endpoint, **kwargs) -> 'FakeResponse':
        return cls(endpoint, content_type='application/json', **kwargs)

    @classmethod
    def timeout(cls, endpoint, **kwargs) -> 'FakeResponse':
        return cls(endpoint, status=GatewayTimeout.code, **kwargs)

    @classmethod
    def from_dict(cls, config: dict) -> 'FakeResponse':
        return cls(**config)

    @staticmethod
    def choice(responses: Iterable['FakeResponse']) -> Optional['FakeResponse']:
        """
        random choice one of responses depends of its chance
        """
        responses = list(responses)
        if responses:
            cum_chance, chances = 0, list()
            for response in responses:
                cum_chance += response.chance
                chances.append(cum_chance)
            rnd_chance = randrange(0, cum_chance)
            for chance, response in zip(chances, responses):
                if chance > rnd_chance:
                    return response
        return None

    def render(self, **kwargs) -> FlaskResponse:
        if self.body_template:
            template = Template(self.body_template)
            template.globals.update(**TEMPLATE_FUNCS)
            body = template.render(**kwargs)
        else:
            body = self.body_template
        return FlaskResponse(
            response=body, status=self.status, headers=self.headers,
            mimetype=self.mimetype, content_type=self.content_type)


class FakeResponseProfile(object):

    responses: DefaultDict[str, List[FakeResponse]]
    state: DefaultDict[str, int]

    def __init__(self, *responses):
        self.responses = defaultdict(list)
        for response in sorted(responses, key=lambda r: r.step):
            self.responses[response.endpoint].append(response)
        self.steps = defaultdict(int)

    def clear(self):
        self.steps.clear()

    def take(self, endpoint: str) -> FakeResponse:
        '''
        sequentially selects requests
        '''
        try:
            if endpoint not in self.responses:
                return None
            responses = self.responses[endpoint]
            step = self.steps[endpoint]
            max_step = responses[-1].step
            step = step % (max_step+1)
            responses = filter(lambda r: r.step == step, responses)
            return FakeResponse.choice(responses)
        finally:
            self.steps[endpoint] += 1
        return FakeResponse(body_template=endpoint)

    @classmethod
    def from_yaml(cls, filename: str) -> 'FakeResponseProfile':
        with open(filename, 'rt', encoding='utf-8') as stream:
            data = yaml.safe_load(stream) or []
        responses = list(FakeResponse.from_dict(config) for config in data)
        return cls(*responses)


class FakeResponseRepository(object):

    def __init__(self, profiles_path: str):
        self.profiles_path = profiles_path
        self.profiles = dict()

    def __getitem__(self, profile: str) -> FakeResponseProfile:
        profile = self.profiles.get(profile)
        if profile is None:
            filename = path.join(self.profiles_path, f'{profile}.yaml')
            if not path.exists(filename):
                raise FileNotFoundError(f'profile: {filename}')
            profile = FakeResponseProfile.from_yaml(filename)
            self.profiles[profile] = profile
        return profile
