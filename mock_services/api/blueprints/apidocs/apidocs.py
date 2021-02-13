from flask import Blueprint, current_app, jsonify

apidocs = Blueprint("apidocs", __name__, static_folder='static')


@apidocs.route('/')
def index():
    return apidocs.send_static_file('index.html')


@apidocs.route('<path:path>')
def static_file(path):
    return apidocs.send_static_file(path)


@apidocs.route("/specs/swagger.json")
def all_spec_file():
    spec = current_app.swagger_specs.all
    return jsonify(spec)


@apidocs.route('/specs/<service>.json')
def service_spec_file(service):
    spec = current_app.swagger_specs[service]
    return jsonify(spec)
