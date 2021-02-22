from dataclasses import asdict, dataclass
from random import randrange
from typing import List, Optional

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
        """ check dataclass asserts """
        if self.step < 0:
            raise ValueError(f'step({self.step} must be positive')
        if self.chance <= 0:
            raise ValueError(f'chance({self.chance}) must be positive')

    def __hash__(self):
        return hash(str(self))

    def render(self, **kwargs) -> FlaskResponse:
        if self.body_template and kwargs:
            template = Template(self.body_template)
            template.globals.update(**TEMPLATE_FUNCS)
            body = template.render(**kwargs)
        else:
            body = self.body_template
        return FlaskResponse(
            response=body, status=self.status, headers=self.headers,
            mimetype=self.mimetype, content_type=self.content_type)

    @classmethod
    def json(cls, endpoint, **kwargs) -> 'FakeResponse':
        return cls(endpoint, content_type='application/json', **kwargs)

    @classmethod
    def text(cls, endpoint, **kwargs) -> 'FakeResponse':
        return cls(endpoint, content_type='text/plain', **kwargs)

    @classmethod
    def timeout(cls, endpoint, **kwargs) -> 'FakeResponse':
        return cls(endpoint, status=GatewayTimeout.code, **kwargs)

    @classmethod
    def from_dict(cls, config: dict) -> 'FakeResponse':
        if not isinstance(config, dict):
            raise ValueError('data is not dict')
        return cls(**config)


class FakeResponseCollection(object):

    """
         lightwear wrapper with helper for manipulate fake_response

         profile.find_endpoint('sms_send').find_step(12).choice()
    """

    def __init__(self, responses: List[FakeResponse] = None):
        self.responses = responses or []

    def __eq__(self, o):
        return isinstance(o, list) and self.responses == o

    def filter_by_endpoint(self, endpoint: str) -> 'FakeResponseCollection':
        """
            find all responses with endpoint
        """
        return FakeResponseCollection(
            [resp for resp in self.responses if resp.endpoint == endpoint])

    def filter_by_step(self, step: int) -> 'FakeResponseCollection':
        """
            find all responses with steps
        """
        # step %= (self.max_step+1)
        return FakeResponseCollection(
            [resp for resp in self.responses if resp.step == step])

    @property
    def max_step(self) -> int:
        return max([resp.step for resp in self.responses], default=0)

    def choice(self) -> Optional['FakeResponse']:
        """
            random choice one of responses depends of its chance
        """
        if self.responses:
            cum_chance, chances = 0, list()
            for response in self.responses:
                cum_chance += response.chance
                chances.append(cum_chance)
            rnd_chance = randrange(0, cum_chance)
            for chance, response in zip(chances, self.responses):
                if chance > rnd_chance:
                    return response
        return None

    def to_data(self):
        return [asdict(resp) for resp in self.responses]

    @classmethod
    def from_list(cls, configs) -> 'FakeResponseCollection':
        if not isinstance(configs, list):
            raise ValueError('data is not list')
        responses = list()
        for config in configs:
            if isinstance(config, FakeResponse):
                responses.append(config)
            elif isinstance(config, dict):
                responses.append(FakeResponse.from_dict(config))
            else:
                raise ValueError(f'Wrong type {type(config)}')
        return cls(responses)
