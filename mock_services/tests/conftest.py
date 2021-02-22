import pytest
from faker import Faker
from redis import Redis

from mock_services.config import MockServicesConfig as confi
from mock_services.models import MockProfile


@pytest.fixture(scope="class")
def fake():
    yield Faker()


@pytest.fixture(scope="session")
def redis():
    yield Redis.from_url(confi.REDIS_URL)


@pytest.fixture()
def mock_profile(redis) -> MockProfile:
    yield MockProfile.create(redis, expire=10)
