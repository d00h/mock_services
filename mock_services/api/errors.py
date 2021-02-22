from mock_services.api.decorators import log_response

from flask import request, Response


def page_not_found(e):
    log_response(request, Response(status=404))
    return e, 404
