"""Manage various git platform profiles"""
import argparse
import inspect
import sys

import hosts
from commons.utils.agents import get_agents
from commons.utils.profiles import delete
from commons.utils.profiles import get_profiles


class Profile:
    @staticmethod
    def get_commands(obj):
        return [m[0].lower() for m in inspect.getmembers(obj, inspect.ismethod) if not m[0].lower().startswith('_')]

    def __init__(self):
        commands_list = Profile.get_commands(self)
        start = 'git_repo profile '
        usage = 'git_repo profile [-v | --verbose]\n'
        for i in commands_list:
            for j in inspect.getdoc(getattr(self, i)).split('\n'):
                usage += '   or: '
                usage += start + i + ' ' + j + '\n'

        parser = argparse.ArgumentParser(usage=usage)
        parser.add_argument('command', nargs='?', help=argparse.SUPPRESS)
        parser.add_argument('--list-agents', action='store_true', default=False, dest='list_agents',
                            help=argparse.SUPPRESS)
        args, unknown = parser.parse_known_args(sys.argv[2:])
        if args.list_agents:
            self.__list_agents()
            exit(0)
        if not args.command:
            self.__list(unknown)
            exit()
        if not hasattr(self, args.command):
            print(
                'git_help: \'%s\' is not a valid command. See \'git_repo profile --help\'.' % args.command)
            exit(1)
        getattr(self, args.command)(unknown)

    def add(self, args):
        """
        <agent> <name> <username>
        """
        parser = argparse.ArgumentParser(
            usage='git_repo profile add [<options>] <agent> <name> <username>')
        parser.add_argument('agent', action='store', nargs='?')
        args, unknown = parser.parse_known_args(args)
        if args.agent is None:
            parser.print_usage()
            exit(1)
        if args.agent not in get_agents():
            print(
                'Invalid agent or agent not supported.\nFor a list of valid agents run: git_hosts profile --list-agents')
            exit(1)
        else:
            getattr(hosts, args.agent).profile.add(unknown)

    def delete(self, args):
        """
        <name>
        """
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('name', action='store', nargs='?')
        parser.parse_args(args)
        args = parser.parse_args(args)
        if not args.name:
            print('No profile name provided')
            exit(1)
        delete(args.name)

    def __list(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', '--verbose',
                            action='store_true', default=False, dest='verbose')
        args = parser.parse_args(args)
        profiles = get_profiles()
        if args.verbose:
            for key, value in profiles.items():
                print('%s\t%s (%s)' % (key, value['username'], value['agent']))
        else:
            print(*list(profiles.keys()), sep='\n')

    def __list_agents(self):
        agents = get_agents()
        print('The available agents are:')
        for i in agents:
            print(i)
