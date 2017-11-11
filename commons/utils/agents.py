import inspect

import hosts


def get_agents():
    return [i[0].lower() for i in inspect.getmembers(hosts, inspect.ismodule)]
