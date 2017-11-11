import configparser
import os


def get_profiles():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.expanduser('~/.git_hosts'), 'profiles'))
    sections = config.sections()
    ret_dict = {}
    for i in sections:
        ret_dict[i] = {'username': config.get(i, 'username'),
                       'agent': config.get(i, 'agent')}
    return ret_dict


def delete(profile):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.expanduser('~/.git_hosts'), 'profiles'))
    if not config.has_section(profile):
        print('Invalid profile name')
        exit(1)
    config.remove_section(profile)
    cfg_file = open(os.path.join(
        os.path.expanduser('~/.git_hosts'), 'profiles'), 'w+')
    config.write(cfg_file)
    cfg_file.close()
    print('Profile deleted')
    exit(0)


def add_profile(agent, name, username, password):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.expanduser('~/.git_hosts'), 'profiles'))
    if name in config:
        config.remove_section(name)
    config.add_section(name)
    config.set(name, 'agent', agent)
    config.set(name, 'username', username)
    config.set(name, 'password', password)
    cfg_file = open(os.path.join(
        os.path.expanduser('~/.git_hosts'), 'profiles'), 'w+')
    config.write(cfg_file)
    cfg_file.close()
