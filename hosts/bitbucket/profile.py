import argparse
from getpass import getpass

import requests

from commons.utils.profiles import add_profile


def add(args):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('name', action='store')
    parser.add_argument('username', action='store')
    args = parser.parse_args(args)
    password = getpass('Enter bitbucket password: ')
    request = requests.get(
        'https://api.bitbucket.org/1.0/user', auth=(args.username, password))
    if request.status_code == 200:
        add_profile('bitbucket', args.name, args.username, password)
        print('Profile created.')
    elif request.status_code == 401:
        print('Invalid Credentials. Please try again.')
    exit(0)
