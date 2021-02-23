from flask import Blueprint, current_app, jsonify

from mock_services.models import MockLogger

mock_logger = Blueprint("mock_logger", __name__,
                        url_prefix='/mock_logger')


@mock_logger.route('', methods=['get'])
def get_logs(**kwargs):
    mock_logger: MockLogger = current_app.mock_logger
    data = list(mock_logger)
    return jsonify(data)


@mock_logger.route('', methods=['delete'])
def clear_logs(**kwargs):
    mock_logger: MockLogger = current_app.mock_logger
    mock_logger.clear()
    return "ok"
