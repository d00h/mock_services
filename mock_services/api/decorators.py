from functools import wraps

from flask import current_app, request, Request, Response 

from mock_services.models import MockProfile, MockLogger


def log_response(request: Request, response : Response):
    mock_logger: MockLogger = current_app.mock_logger
    mock_logger.add(request.endpoint,
                    request={
                       'method': request.method,
                       'url': request.url,
                       'headers': request.headers,
                       'data': request.get_data(as_text=True),
                    },
                    response={
                       "status": response.status,
                       "data": response.get_data(as_text=True),
                    })


def mockable(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        mock_profile: MockProfile = current_app.mock_profile
        fake_response = mock_profile.next_response(request.endpoint)
        if fake_response is not None:
            flask_response = fake_response.render(*args, **kwargs)
        else:
            flask_response = func(*args, **kwargs)
        log_response(request, flask_response)
        return flask_response
    return decorated_function
