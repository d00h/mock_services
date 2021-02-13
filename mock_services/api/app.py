import logging
from typing import Optional

from flask import Flask, Response
from flask.app import setupmethod
from flask.globals import LocalProxy
from flask.logging import default_handler

from mock_services.models import FakeRepository, SwaggerSpecRepository

from .blueprints.root import root
from .blueprints.apidocs import apidocs
from .blueprints.service.easysms import easysms
from .blueprints.service.mailgun import mailgun


class MockServicesApp(Flask):

    repository: FakeRepository
    swagger_spec: SwaggerSpecRepository

    def __init__(self):
        Flask.__init__(self, __name__)

    @setupmethod
    def setup_app(self):
        self._init_logger()
        self._init_repositories()

    # @setupmethod
    # def _init_config(self):
    #     # TODO: Flast.config_class => Confi
    #     self.confi = config.Config
    #     self.config.from_object(self.confi)

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

    def _init_repositories(self):
        self.fake_responses = FakeRepository('/app/profiles')
        self.swagger_specs = SwaggerSpecRepository('/app/specs')

    def get_fake_response(
            self, profile: str, endpoint: str, **kwargs) -> Optional[Response]:
        session = self.fake_responses[profile]
        response = session.take(endpoint)
        if response is not None:
            return response.render(**kwargs)
        return None


def create_app() -> MockServicesApp:
    app = MockServicesApp()
    app.setup_app()

    app.register_blueprint(root, url_prefix='/')
    app.register_blueprint(apidocs, url_prefix='/apidocs')
    app.register_blueprint(easysms, url_prefix='/service/<profile>/easysms')
    app.register_blueprint(mailgun, url_prefix='/service/<profile>/mailgun')

    return LocalProxy(lambda: app)
