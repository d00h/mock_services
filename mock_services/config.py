from confi import BaseEnvironConfig, ConfigField


class Config(BaseEnvironConfig):

    COMMIT_HASH = ConfigField(required=True)
    COMMIT_MESSAGE = ConfigField(required=True)
