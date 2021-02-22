from confi import BaseEnvironConfig, BooleanConfig, ConfigField, IntConfig


def weeks(value):
    return value * 7 * 24 * 60


def minutes(value):
    return value * 60


class MockServicesConfig(BaseEnvironConfig):

    HOST = ConfigField(default='0.0.0.0')
    PORT = IntConfig(default=5000)
    DEBUG = BooleanConfig(default=False)

    COMMIT_HASH = ConfigField()
    COMMIT_MESSAGE = ConfigField()

    REDIS_URL = ConfigField()
    REDIS_EXPIRE = IntConfig(default=weeks(1))
