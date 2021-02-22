from covador.flask import args
from flask import Blueprint, current_app, jsonify, request

from mock_services.models import MockProfile

mock_profile = Blueprint("mock_profile", __name__,
                         url_prefix='/mock_profile')


@mock_profile.route('', methods=['get'])
def get_mock_profile(**kwargs):
    mock_profile: MockProfile = current_app.mock_profile
    data = mock_profile.config.to_data()
    return jsonify(data)


@mock_profile.route('', methods=['post'])
def post_mock_profile(**kwargs):
    config_data = request.get_json(force=True)
    mock_profile: MockProfile = current_app.mock_profile
    mock_profile.config = config_data
    return "ok"
