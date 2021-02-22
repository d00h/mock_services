import sys
from argparse import ArgumentParser
from os import path
from urllib.parse import urlencode

import requests

parser = ArgumentParser()
parser.add_argument("--host", action="store",
                    nargs="?",
                    default="http://127.0.0.1:5400",
                    help="http://127.0.0.1:5400")
parser.add_argument("--count", action="store", type=int)


def process(url, count):
    q = {
        'login': 'username',
        'password': '12345',
        'ordinator': '+7-905-123-45-67',
        'phone': '+7-905-999-99-99',
        'text': 'hello world'
    }
    url = path.join(url, 'service/easysms', '?'+urlencode(q))
    for _ in range(count):
        print(url)
        response = requests.get(url)
        print(response.status_code, response.text)
        print()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        process(args.host, args.count)
