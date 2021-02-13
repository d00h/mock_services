from copy import copy
from fnmatch import fnmatch
from os import listdir, path

import yaml


class SwaggerSpecRepository(object):

    """
        store swagger specs for apidocs
    """

    def __init__(self, folder: str):
        self.folder = folder

    def __getitem__(self, service: str) -> dict:
        filename = path.join(self.folder, f'{service}.yaml')
        if not path.exists(filename):
            raise FileNotFoundError(f'spec: {filename}')
        with open(filename, 'rt', encoding='utf-8') as stream:
            return yaml.safe_load(stream) or {}

    @staticmethod
    def _add_prefix_path(spec: dict) -> dict:
        prefix = '/service/{profile}'
        parameter = {
            'in': 'path',
            'name': 'profile',
            'type': 'string',
            'required': True,
            'default': 'default'
        }
        old_paths, new_paths = spec.get('paths', {}), {}
        for old_uri, old_methods in old_paths.items():
            new_uri = path.join('/service/{profile}', old_uri.lstrip('/'))
            new_methods = copy(old_methods)
            new_paths[new_uri] = new_methods
            for body in new_methods.values():
                if 'parameters' in body:
                    body['parameters'].insert(0, parameter)
                else:
                    body['parameters'] = [parameter]
        return {
            'paths': new_paths,
            'tags': spec.get('tags', [])
        }

    @property
    def all(self) -> dict:
        paths, tags = dict(), list()
        for filename in listdir(self.folder):
            if not fnmatch(filename, '*.yaml'):
                continue
            service, _ = path.splitext(filename)
            spec = self._add_prefix_path(self[service])
            paths.update(spec.get('paths', {}))
            tags.extend(spec.get('tags', []))
        return {
            'swagger': '2.0',
            'info': {'title': 'MockServices'},
            'consumes': ['application/json'],
            'produces': ['application/json'],
            'schemes': ['http', 'https'],
            'paths': paths,
            'tags': tags
        }
