import argparse
from getpass import getpass

import requests

from commons.utils.profiles import add_profile


def add(args):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('name', action='store')
    parser.add_argument('username', action='store')
    args = parser.parse_args(args)
    password = getpass('Enter github password: ')
    request = requests.get('https://api.github.com/user', auth=(args.username, password),
                           headers={'Accept': 'application/vnd.github.v3.raw+json'})
    if request.status_code == 200:
        add_profile('github', args.name, args.username, password)
        print('Profile created.')
    elif request.json()['message'] == 'Bad credentials':
        print('Invalid Credentials. Please try again.')
    exit(0)
