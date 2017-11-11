# -*- coding: utf-8 -*-
import os

from commons.utils.arg_parser import Gateway

if __name__ == '__main__':
    os.makedirs(os.path.join(os.path.expanduser(
        '~'), '.git_repo'), exist_ok=True)
    Gateway()
