from copy import copy
from fnmatch import fnmatch
from os import listdir, path
from typing import Iterable

import yaml


class SwaggerSpec(object):

    """
      dirty class with helpers for swagger 2.0
    """

    info: dict
    consumes: list
    produces: list
    schemes: list
    paths: dict
    tags: list
    components_schemas: dict

    def __init__(self, info: dict = None, consumes: list = None, produces: list = None,
                 schemas: list = None, paths: dict = None, tags: list = None,
                 components_schemas: dict = None):
        self.info = info or dict()
        self.consumes = consumes or ['application/json']
        self.produces = produces or ['application/json']
        self.schemes = schemas or ['http', 'https']
        self.paths = paths or dict()
        self.tags = tags or list()
        self.components_schemas = components_schemas or dict()

    def append_path_prefix(self, *word):
        """ add prefix to all paths"""
        prefix = path.join(*word)
        old_paths, new_paths = self.paths, {}
        for old_uri, old_methods in old_paths.items():
            new_uri = path.join(prefix, old_uri.lstrip('/'))
            new_methods = copy(old_methods)
            new_paths[new_uri] = new_methods
        self.paths = new_paths

    def append_parameter(self, parameter: dict):
        """ add parameter to all paths """
        paths = copy(self.paths)
        for _, methods in paths.items():
            for body in methods.values():
                if 'parameters' in body:
                    body['parameters'].insert(0, parameter)
                else:
                    body['parameters'] = [parameter]
        self.paths = paths

    def append_spec(self, spec: 'SwaggerSpec'):
        self.paths.update(spec.paths)
        self.components_schemas.update(spec.components_schemas)
        self.tags.extend(spec.tags)

    def to_dict(self) -> dict:
        return {
            'swagger': '2.0',
            'info': self.info,
            'consumes': self.consumes,
            'produces': self.produces,
            'schemes': self.schemes,
            'paths': self.paths,
            'tags': self.tags,
            'components': {'schemas': self.components_schemas}
        }

    @classmethod
    def from_yaml(cls, filename):
        if not path.exists(filename):
            raise FileNotFoundError(f'spec: {filename}')
        with open(filename, 'rt', encoding='utf-8') as stream:
            return yaml.safe_load(stream) or {}


class SwaggerSpecRepository(object):

    """
        store swagger specs for apidocs
    """

    def __init__(self, folder: str):
        self.folder = folder

    def __getitem__(self, blueprint: str) -> SwaggerSpec:
        """ swagger of mock_services server  """
        filename = path.join(self.folder, f'{blueprint}.yaml')
        return SwaggerSpec.from_yaml(filename)

    def __iter__(self) -> Iterable[str]:
        for filename in listdir(self.folder):
            if not fnmatch(filename, '*.yaml'):
                continue
            name, _ = path.splitext(filename)
            yield name


class SwaggerAggregator(object):

    def __init__(self, root_swagger_folder: str):
        service_swagger_folder = path.join(root_swagger_folder, 'service')
        self.service = SwaggerSpecRepository(service_swagger_folder)
        self.system = SwaggerSpecRepository(root_swagger_folder)

    def to_dict(self) -> dict:
        result = SwaggerSpec(info={'title': 'MockServices'})
        result.append_spec(self.system['profile'])
        profile_in_path = {
            'in': 'path',
            'name': 'profile',
                    'type': 'string',
                    'required': True,
                    'default': 'default'
        }
        for name in self.service:
            external_service = self.service[name]
            external_service.append_path_prefix('service', name)
            external_service.append_parameter(profile_in_path)

            result.append_spec(external_service)
        return result.to_dict()
