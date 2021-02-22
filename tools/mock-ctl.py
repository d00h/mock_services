import sys
from abc import ABC, abstractclassmethod, abstractmethod
from argparse import ArgumentParser
from argparse import Namespace as ArgumentNamespace
from os import path

import requests
import yaml

SERVERS = {
    'local': 'http://127.0.0.1:5400',
    'dev': 'http://192.168.1.2:5000',
}
# --------------------------------------------------------


class ConsoleWriter(ABC):

    @abstractmethod
    def write(self, *items):
        pass


class RawConsoleWriter(object):

    def write(self, *items):
        print(' '.join(items))


class TableConsoleWriter(object):

    def __init__(self, columns: list):
        self.width = columns

    def _format(self, column, item) -> str:
        if column < len(self.width):
            template = '{{:{0}}}'.format(self.width[column])
            return template.format(item)
        return item

    def write(self, *items):
        print(' '.join([self._format(column, item)
                        for column, item in enumerate(items)]))

# --------------------------------------------------------


class Command(ABC):

    @abstractclassmethod
    def configure_parser(cls, parser: ArgumentParser):
        pass

    def create_writer(self, args: ArgumentNamespace) -> ConsoleWriter:
        return TableConsoleWriter(columns=[8, 20])

    @abstractmethod
    def run(self, args: ArgumentNamespace, out: ConsoleWriter):
        pass


class ListServers(Command):

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        parser.set_defaults(create_command=cls)

    def run(self,  args: ArgumentNamespace, out: ConsoleWriter):
        out.write('Alias', 'Host')
        for server_alias, server_host in SERVERS.items():
            out.write(server_alias, server_host)


class ListProfiles(Command):

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        parser.set_defaults(create_command=cls)

    def run(self,  args: ArgumentNamespace, out: ConsoleWriter):
        print("list profiles")
        out.write('Alias', 'Host')


class ListLogs(Command):

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        parser.set_defaults(create_command=cls)

    def run(self,  args: ArgumentNamespace, out: ConsoleWriter):
        print("list logs")


class PutProfile(Command):

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        parser.add_argument("filename")
        parser.add_argument("-o", "--output", default="local")
        parser.set_defaults(create_command=cls)

    def run(self,  args: ArgumentNamespace, out: ConsoleWriter):
        print("put_profile")
        with open(args.filename) as stream:
            data = yaml.safe_load(stream)
        url = path.join(SERVERS[args.output], "mock_profile")
        resp = requests.post(url, json=data)
        print(url, resp.status_code)


class GetProfile(Command):

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        parser.set_defaults(create_command=cls)

    def run(self,  args: ArgumentNamespace, out: ConsoleWriter):
        print("get_profile")


class DeleteProfile(Command):

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        parser.set_defaults(create_command=cls)

    def run(self,  args: ArgumentNamespace, out: ConsoleWriter):
        print("delete_profile")


def main():
    parser = ArgumentParser()
    subs = parser.add_subparsers()
    for key, command in {
        'list-servers':   ListServers,
        'list-profiles':  ListProfiles,
        'put-profile':    PutProfile,
        'delete-profile': DeleteProfile,
        'get-profile':    GetProfile,
        'list-logs':      ListLogs,
    }.items():
        sub_parser = subs.add_parser(key)
        command.configure_parser(sub_parser)

    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        command = args.create_command()
        writer = command.create_writer(args)
        command.run(args, out=writer)


if __name__ == '__main__':
    main()
