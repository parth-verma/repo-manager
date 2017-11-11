import argparse
import inspect
import sys

from commons import commands


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        pass


class Gateway:
    def get_commands(self):
        return [m[0].lower() for m in inspect.getmembers(commands, inspect.isclass) if
                m[1].__module__.startswith('commons.commands.')]

    def __init__(self):
        commands_list = self.get_commands()
        usage = 'git_repo <command> [<args>]\n\nSome useful commands are:\n'

        for i in commands_list:
            usage += '  %s%s\n' % (i.ljust(14),
                                   inspect.getdoc(getattr(commands, i)))

        parser = argparse.ArgumentParser(
            description='Git repository manager',
            usage=usage)
        parser.add_argument('command', help='Subcommand to run', nargs='?')
        args = parser.parse_args(sys.argv[1:2])
        if not args.command:
            parser.print_usage()
            exit(0)
        if not hasattr(commands, args.command):
            print(
                'git_help: \'%s\' is not a valid command. See \'git_repo --help\'.' % args.command)
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(commands, args.command.title())()

    def commit(self):
        parser = argparse.ArgumentParser(
            description='Record changes to the repository')
        # prefixing the argument with -- means it's optional
        parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        print('Running git commit, amend=%s' % args.amend)

    def fetch(self):
        parser = argparse.ArgumentParser(
            description='Download objects and refs from another repository')
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('repository')
        args = parser.parse_args(sys.argv[2:])
        print('Running git fetch, repository=%s' % args.repository)
