import logging
from typing import Optional

import redis
from flask import Flask, Response
from flask.app import setupmethod
from flask.globals import LocalProxy
from flask.logging import default_handler

from mock_services.api.blueprints.apidocs import apidocs
from mock_services.api.blueprints.root import root
from mock_services.api.blueprints.service import cloudpayments, easysms, mailgun
from mock_services.config import MockServicesConfig
from mock_services.models import FakeResponseRepository, SwaggerSpecRepository


class MockServicesApp(Flask):

    fake_responses: FakeResponseRepository
    swagger_specs: SwaggerSpecRepository

    def __init__(self, config):
        Flask.__init__(self, __name__)
        self.config.update(config)

    @setupmethod
    def setup_app(self):
        self._init_logger()
        self._init_repositories()
        self._init_redis()

    def _init_logger(self):
        self.logger.removeHandler(default_handler)

        log_level = logging.DEBUG
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        )

        handler = logging.StreamHandler()
        handler.setLevel(log_level)
        handler.setFormatter(formatter)

        self.logger.setLevel(log_level)
        self.logger.addHandler(handler)

    def _init_redis(self):
        r = redis.Redis(host=self.config['REDIS_HOST'],
                        port=self.config['REDIS_PORT'],
                        db=self.config['REDIS_PROFILE_CONFIG_DB'])
        r.get('111')

    def _init_repositories(self):
        self.fake_responses = FakeResponseRepository('/app/profiles')
        self.swagger_specs = SwaggerSpecRepository('/app/specs')

    def get_fake_response(
            self, profile: str, endpoint: str, **kwargs) -> Optional[Response]:
        session = self.fake_responses[profile]
        response = session.take(endpoint)
        if response is not None:
            return response.render(**kwargs)
        return None


def create_app() -> MockServicesApp:
    app = MockServicesApp(config=MockServicesConfig.as_dict())
    app.setup_app()
    app.register_blueprint(root, url_prefix='/')
    app.register_blueprint(apidocs, url_prefix='/apidocs')
    app.register_blueprint(easysms, url_prefix='/service/easysms')
    app.register_blueprint(mailgun, url_prefix='/service/mailgun')
    app.register_blueprint(cloudpayments, url_prefix='/service/cloudpayments')

    return LocalProxy(lambda: app)
