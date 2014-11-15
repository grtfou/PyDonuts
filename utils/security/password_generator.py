#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20130602
'''
Generate random string
'''
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import time
import string
import random

def get_random_pwd(length=32):
    '''
    Random string (only a-z and 0-9)
    '''
    hash_str = '{{0:0{}x}}'.format(length)
    return hash_str.format(random.randrange(16**length))

def get_random_str(length=20):
    '''
    Generate random string (a-z, A-Z and 0-9)
    '''
    hash_choice = string.digits + string.ascii_letters
    return ''.join([random.choice(hash_choice) for _ in range(length)])


if __name__ == '__main__':
    print(get_random_pwd())
    print(get_random_str())

    time.sleep(10)
