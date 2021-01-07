from typing import Iterable, Tuple

import yaml
from flask import Blueprint, current_app, jsonify, redirect
from werkzeug.routing import Rule

apidocs = Blueprint("apidocs", __name__, static_folder='static')


def list_path_spec() -> Iterable[Tuple[str, str, dict]]:
    """
    list all routes with yaml docs
    -> [url, method, yaml_spec]
    """
    for rule in current_app.url_map.iter_rules():  # type: Rule
        try:
            url = rule.rule.replace('<', '{').replace('>', '}')
            func = current_app.view_functions.get(rule.endpoint)
            if func and func.__doc__:
                path_spec = yaml.safe_load(func.__doc__)
                path_spec['operationId'] = rule.endpoint
                for method in rule.methods:
                    yield url, method.lower(), path_spec
        except yaml.scanner.ScannerError:
            continue

def list_tags_spec() -> Iterable[dict]:
    """
    """
    for blueprint in current_app.blueprints.values():  # type: Blueprint
        try:
            if hasattr(blueprint, 'swagger_tag'):
                tag_spec = yaml.safe_load(blueprint.swagger_tag)
                yield tag_spec
        except yaml.scanner.ScannerError:
            continue

def create_spec() -> dict:
    paths = dict()
    for uri, method, spec in list_path_spec():
        if method not in ['get', 'post', 'delete']:
            continue
        if uri not in paths:
            paths[uri] = dict()
        paths[uri][method] = spec
    return {
        'swagger': '2.0',
        'info': {'title': 'MockServices'},
        'consumes': ['application/json'],
        'produces': ['application/json'],
        'schemes': ['http', 'https'],
        'paths': paths,
        'tags': list(list_tags_spec())
    }


@apidocs.route("/")
def index():
    return redirect('index.html')


@apidocs.route("/swagger.json")
def swagger():
    spec = create_spec()
    return jsonify(spec)


@apidocs.route('/<path:path>')
def send_file(path):
    return apidocs.send_static_file(path)
