import logging

from flask import Flask
from flask.globals import LocalProxy
from flask.logging import default_handler
from redis import Redis

from mock_services.api.blueprints.apidocs import apidocs
from mock_services.api.blueprints.root import root
from mock_services.api.blueprints.mock_profiles import mock_profiles
from mock_services.api.blueprints.service import cloudpayments, easysms, mailgun
from mock_services.config import MockServicesConfig as confi
from mock_services.models import MockService, SwaggerAggregator


class MockServicesApp(Flask):

    swagger: SwaggerAggregator
    mock_service: MockService

    def __init__(self):
        Flask.__init__(self, __name__, static_folder='static')

    def init_logger(self):
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

    def init_mock_service(self, redis_url, redis_expire):
        redis = Redis.from_url(redis_url)
        self.mock_service = MockService(redis, redis_expire)

    def init_swagger(self, folder):
        self.swagger = SwaggerAggregator(folder)


def create_app() -> MockServicesApp:
    app = MockServicesApp()
    app.config.update(confi.as_dict())

    app.init_logger()
    app.init_mock_service(confi.REDIS_URL, confi.REDIS_EXPIRE)
    app.init_swagger('/app/specs')

    app.register_blueprint(root)
    app.register_blueprint(apidocs)
    app.register_blueprint(mock_profiles)
    app.register_blueprint(easysms)
    app.register_blueprint(mailgun)
    app.register_blueprint(cloudpayments)

    return LocalProxy(lambda: app)
