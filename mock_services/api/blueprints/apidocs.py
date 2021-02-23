from flask import Blueprint, current_app, jsonify

apidocs = Blueprint("apidocs", __name__,
                    url_prefix='/apidocs')


@apidocs.route('/')
def aggregate_index():
    return current_app.send_static_file('index.html')


@apidocs.route('/static/<path:path>')
def aggregate_static(path):
    return current_app.send_static_file(path)


@apidocs.route('/swagger.json')
def aggregate_spec():
    spec = current_app.swagger.to_dict()
    return jsonify(spec)


@apidocs.route('/<service>/')
def service_index(service):
    return current_app.send_static_file('index.html')


@apidocs.route('/<service>/swagger.json')
def service_spec(service):
    spec = current_app.swagger.service[service].to_dict()
    return jsonify(spec)


@apidocs.route('/<service>/static/<path:path>')
def service_static(service, path):
    return current_app.send_static_file(path)

