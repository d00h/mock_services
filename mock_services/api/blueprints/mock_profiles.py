from covador.flask import args
from flask import Blueprint, current_app, jsonify, request

from mock_services.models import MockService

mock_profiles = Blueprint("mock_profile", __name__,
                          url_prefix='/mock_profile')


@mock_profiles.route('/', methods=['get'])
def list_mock_profile(**kwargs):
    mock_service: MockService = current_app.mock_service
    profiles = list(mock_service.find_profiles())
    return jsonify(profiles)


@mock_profiles.route('<profile>', methods=['get'])
@args(profile=str)
def get_mock_profile_config(profile, **kwargs):
    mock_service: MockService = current_app.mock_service
    mock_profile = mock_service.get_profile(profile)
    return jsonify(mock_profile.config.to_data())


@mock_profiles.route('<profile>', methods=['put'])
@args(profile=str)
def data_mock_profile_config(profile, **kwargs):
    config_data = request.get_json(force=True)
    mock_service: MockService = current_app.mock_service
    mock_profile = mock_service.get_profile(profile)
    mock_profile.config = config_data
    return "ok"
