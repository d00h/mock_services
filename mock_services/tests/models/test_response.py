from collections import Counter

import pytest

from mock_services.models import FakeResponse, FakeSession


def test_response_choice(fake):
    resp1 = FakeResponse.timeout(endpoint=fake.word(), chance=50)
    resp2 = FakeResponse.json(endpoint=fake.word(), chance=50)
    resp3 = FakeResponse.json(endpoint=fake.word(), chance=50)

    variants = [resp1, resp2, resp3]
    results = list(FakeResponse.choice(variants) for _ in range(1000))
    assert resp1 in results
    assert resp2 in results
    assert resp3 in results


def test_response_choice_empty():
    assert FakeResponse.choice([]) is None


def test_wrong_response_chance(fake):
    with pytest.raises(ValueError):
        FakeResponse(endpoint=fake.word(), chance=0)


def test_wrong_response_step(fake):
    with pytest.raises(ValueError):
        FakeResponse(endpoint=fake.word(), step=-1)


def test_session_step_by_step(fake):
    endpoint = fake.word()
    resp0 = FakeResponse.json(endpoint=endpoint, step=0)
    resp1 = FakeResponse.timeout(endpoint=endpoint, step=1)
    resp3 = FakeResponse.timeout(endpoint=endpoint, step=3)
    session = FakeSession(resp0, resp1, resp3)
    for _ in range(2):
        assert session.take(endpoint) == resp0
        assert session.take(endpoint) == resp1
        assert session.take(endpoint) is None
        assert session.take(endpoint) == resp3


def test_session_step_by_step_cleared(fake):
    endpoint = fake.word()
    resp0 = FakeResponse.json(endpoint=endpoint, step=0)
    resp1 = FakeResponse.timeout(endpoint=endpoint, step=1)
    resp3 = FakeResponse.timeout(endpoint=endpoint, step=3)
    session = FakeSession(resp0, resp1, resp3)
    for _ in range(2):
        session.clear()
        assert session.take(endpoint) == resp0
        assert session.take(endpoint) == resp1


def test_session_choice_by_chance(fake):
    endpoint = fake.word()
    resp90 = FakeResponse.json(endpoint=endpoint, chance=90)
    resp10 = FakeResponse.timeout(endpoint=endpoint, chance=10)
    resp_other_endpoint = FakeResponse.timeout(endpoint=fake.word())
    session = FakeSession(resp90, resp10, resp_other_endpoint)
    result = list()
    for _ in range(1000):
        result.append(session.take(endpoint))
    counter = Counter(result)
    assert counter[resp90] > 0
    assert counter[resp10] > 0
    assert counter[resp90] > counter[resp10]
    assert counter[resp_other_endpoint] == 0
    assert session.take(resp_other_endpoint.endpoint) == resp_other_endpoint
