"""
# Generated from {{ filename }}
from flask import Blueprint, current_app, jsonify

{{ service }} = Blueprint("{{ service }}", __name__)
{% for route in paths %}

@{{ service }}.route('{{ route.path }}',
                     endpoint='{{ service }}.{{ route.endpoint }}',
                     methods=['{{ route.method }}'])
def {{ route.endpoint }}(**kwargs):
    return current_app.get_fake_response(**kwargs) or jsonify({})
{% endfor %}
"""
import re
import sys
from argparse import ArgumentParser
from os import path
from typing import Iterable

import jinja2
import yaml

parser = ArgumentParser()
parser.add_argument("input", help="spec file")
parser.add_argument("-o", "--output", action="store",
                    nargs="?", help="python file")


def list_paths(input_filename: str) -> Iterable[dict]:
    """
        return { path , method, operationId }
    """
    service, _ = path.splitext(path.basename(input_filename))
    with open(input_filename, "rt", encoding="utf-8") as stream:
        spec = yaml.safe_load(stream)
    for uri, methods in spec.get('paths', {}).items():
        for method, body in methods.items():
            operation_id = body.get('operationId')
            if operation_id is None:
                raise KeyError(f'{uri} without operationId')
            match = re.match(r"^([^\.]+)\.([\w_]+)$", operation_id, re.M)
            if not match:
                raise KeyError(f'{uri} wrong operationId format {operation_id}')
            if match.group(1) != service:
                raise KeyError(f'{uri} wrong operationId "{service}" != "{match.group(1)}"')
            yield {'path': uri, 'method': method, 'endpoint': match.group(2)}


def process(input_filename: str, output_stream):
    template = jinja2.Template(__doc__)
    service, _ = path.splitext(path.basename(input_filename))
    result = template.render({
        "filename": input_filename,
        "service": service,
        "paths": list_paths(input_filename)
    })
    print(result, file=output_stream)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        if args.output is None:
            process(args.input, sys.stdout)
        else:
            with open(args.output, "wt") as out_stream:
                process(args.input, out_stream)
