from collections import Counter

import pytest

from mock_services.models.fake_response import FakeResponse, FakeResponseCollection


class TestFakeResponse(object):

    @pytest.fixture(autouse=True)
    def setup(self, fake):
        self.fake = fake

    def test_create_wrong_step(self):
        negative_step = self.fake.random_int(min=-100, max=-1)
        with pytest.raises(ValueError):
            FakeResponse(endpoint=self.fake.word(), step=negative_step)

    def test_create_wrong_chance(self):
        negative_chance = self.fake.random_int(min=-100, max=0)
        with pytest.raises(ValueError):
            FakeResponse(endpoint=self.fake.word(), chance=negative_chance)

    def test_render_json(self):
        value = self.fake.word()
        fake_response = FakeResponse(endpoint=self.fake.word(),
                                     status=201,
                                     content_type='application/json',
                                     body_template=f'{{ "name": "{value}" }}')
        flask_response = fake_response.render()
        assert flask_response.status_code == fake_response.status
        assert flask_response.json == {"name": value}

    def test_from_dict(self):
        endpoint = self.fake.word()
        response = FakeResponse.from_dict({'endpoint': endpoint, 'status': 204})

        assert response.endpoint == endpoint
        assert response.status == 204


class TestFakeResponseCollection(object):

    @pytest.fixture(autouse=True)
    def setup(self, fake):
        self.fake = fake

    def test_usage(self):
        profile = FakeResponseCollection([
            FakeResponse.json(endpoint=self.fake.word()),
            FakeResponse.json(endpoint='sms_send'),
            FakeResponse.json(endpoint='email_send', body_template={'sended': True})
        ])
        profile.filter_by_endpoint('sms_send').filter_by_step(1).choice()

    def test_eq(self):
        resp0 = FakeResponse.timeout(endpoint=self.fake.word(), step=0)
        resp2 = FakeResponse.json(endpoint=self.fake.word(), step=2)

        collection = FakeResponseCollection([resp0, resp2])
        assert collection == [resp0, resp2]

    def test_max_step(self):

        resp0 = FakeResponse.timeout(endpoint=self.fake.word(), step=0)
        resp2 = FakeResponse.json(endpoint=self.fake.word(), step=2)

        collection = FakeResponseCollection([resp0, resp2])
        assert collection.max_step == 2

    def test_filter_by_endpoint(self):
        endpoint1, endpoint2 = self.fake.word(), self.fake.word()
        resp11 = FakeResponse.timeout(endpoint=endpoint1, step=0)
        resp12 = FakeResponse.timeout(endpoint=endpoint1, step=0)
        resp21 = FakeResponse.json(endpoint=endpoint2, step=2)

        collection = FakeResponseCollection([resp11, resp12, resp21])

        assert collection.filter_by_endpoint(endpoint1) == [resp11, resp12]
        assert collection.filter_by_endpoint(endpoint2) == [resp21]
        assert collection.filter_by_endpoint(self.fake.word()) == []

    def test_filter_by_step(self):
        resp0 = FakeResponse.timeout(endpoint=self.fake .word(), step=0)
        resp2 = FakeResponse.json(endpoint=self.fake .word(), step=2)

        collection = FakeResponseCollection([resp0, resp2])
        assert collection.filter_by_step(0) == [resp0]
        assert collection.filter_by_step(1) == []
        assert collection.filter_by_step(2) == [resp2]
        assert collection.filter_by_step(4) == []

    def test_choice_chances(self):
        endpoint = self.fake .word()
        resp90 = FakeResponse.json(endpoint=endpoint, chance=90)
        resp10 = FakeResponse.timeout(endpoint=endpoint, chance=10)
        collection = FakeResponseCollection([resp90, resp10])
        result = list()
        for _ in range(1000):
            result.append(collection.choice())
        counter = Counter(result)
        assert counter[resp90] > 0
        assert counter[resp10] > 0
        assert counter[resp90] > counter[resp10]

    def test_choice_empty(self):
        collection = FakeResponseCollection()
        assert collection.choice() is None
