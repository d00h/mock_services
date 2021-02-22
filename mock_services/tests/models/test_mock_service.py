import pytest
from faker import Faker

from mock_services.models import FakeResponse, MockProfile


class TestMockService(object):

    fake: Faker
    mock_profile: MockProfile

    @pytest.fixture(autouse=True)
    def setup(self, fake, mock_service):
        self.fake = fake
        self.mock_service = mock_service

    @staticmethod
    def execute_request(profile, endpoint):
        fake_response = profile.next_response(endpoint)
        flask_response = fake_response.render()
        return flask_response.get_data(as_text=True)

    def test_usage(self):
        profile = self.mock_service.get_profile(self.fake.word())
        endpoint1, endpoint2 = self.fake.word(), self.fake.word()
        text1, text2 = self.fake.word(), self.fake.word()
        profile.config = [
            FakeResponse.text(endpoint=endpoint1, body_template=text1),
            FakeResponse.text(endpoint=endpoint2, body_template=text2),
        ]

        assert self.execute_request(profile, endpoint1) == text1
        assert self.execute_request(profile, endpoint2) == text2
        assert self.execute_request(profile, endpoint1) == text1
