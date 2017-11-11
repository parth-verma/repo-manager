import argparse
from getpass import getpass

import requests

from commons.utils.profiles import add_profile


def add(args):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('name', action='store')
    parser.add_argument('username', action='store')
    args = parser.parse_args(args)
    password = getpass('Enter gitlab password: ')
    request = requests.post('https://gitlab.com/oauth/token', json={'grant_type': 'password',
                                                                    'username': args.username,
                                                                    'password': password})
    if request.status_code == 200:
        add_profile('gitlab', args.name, args.username, password)
        print('Profile created.')
    elif request.status_code == 401:
        print('Invalid Credentials. Please try again.')
    exit(0)
