from confi import BaseEnvironConfig, BooleanConfig, ConfigField, IntConfig


class MockServicesConfig(BaseEnvironConfig):

    HOST = ConfigField(default='0.0.0.0')
    PORT = IntConfig(default=5000)
    DEBUG = BooleanConfig(default=False)

    COMMIT_HASH = ConfigField()
    COMMIT_MESSAGE = ConfigField()

    REDIS_HOST = ConfigField(required=True)
    REDIS_PORT = IntConfig(default=6379)
    REDIS_PROFILE_CONFIG_DB = IntConfig(default=0)
    REDIS_PROFILE_LOG_DB = IntConfig(default=1)
