from flask import Blueprint, current_app, jsonify, request

from mock_services.models import FakeResponseCollection, MockProfile

mock_profile = Blueprint("mock_profile", __name__,
                         url_prefix='/mock_profile')


@mock_profile.route('', methods=['get'])
def get_profile(**kwargs):
    mock_profile: MockProfile = current_app.mock_profile
    data = mock_profile.config.to_data()
    return jsonify(data)


@mock_profile.route('', methods=['post'])
def set_profile(**kwargs):
    data = request.get_data()
    config_data = FakeResponseCollection.try_parse(data)
    if config_data is None:
        raise Exception(data)
    mock_profile: MockProfile = current_app.mock_profile
    mock_profile.config = config_data
    return "ok"


@mock_profile.route('', methods=['delete'])
def delete_profile(**kwargs):
    mock_profile: MockProfile = current_app.mock_profile
    mock_profile.config = None
    return "ok"
