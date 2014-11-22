#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20120821
#  @date          20141123 - For PEP8 format
"""
Search file to rename new filename
"""
from __future__ import unicode_literals
from __future__ import print_function

import os
import re
import random

class FastRename(object):
    '''
    File rename for regex
    '''

    def __init__(self):
        pass

    @classmethod
    def list_files(cls, is_include_sub=False):
        '''
        Visit file(folder) path by regex
        '''
        search_file_list = []
        for dirname, _, filenames in os.walk(os.getcwd()):
            for filename in filenames:
                tree_path = os.path.join(dirname, filename)
                search_file_list.append(tree_path)

            if not is_include_sub:
                return search_file_list

        return search_file_list


    def rename(self, search_exp, replace_exp, **kwargs):
        '''
        Main function for rename the file
        '''
        settings = {'is_prod': False,
                    'is_include_sub': False,
                    'search_type': "xml"}

        for name, value in kwargs.items():
            settings[name] = value

        ### travel path ###
        for work_path in self.list_files(settings['is_include_sub']):
            # old file name and path
            dir_path = b'{}{}'.format(os.sep.join(work_path.split(os.sep)[:-1]),
                                      os.sep)

            # Search rule
            find_rule = r"({})\.{}$".format(search_exp, settings['search_type'])
            find_file_path = re.search(find_rule, work_path.split(os.sep)[-1])

            if find_file_path:
                print(b"Old Path: {}".format(work_path))

                # Checking filename for replace new name
                new_name_set = re.search(replace_exp, find_file_path.group(1))

                if new_name_set:
                    new_path = b'{}{}.{}'.format(dir_path,
                                                 new_name_set.group(1),
                                                 settings['search_type'])
                    new_path_no_ext = b'{}{}'.format(dir_path,
                                                     new_name_set.group(1))

                    # Avoid replace the same name file
                    if os.path.exists(new_path):
                        new_path = b'{}_{}.{}'.format(new_path_no_ext,
                                                      str(random.randint(1, 99)),
                                                      settings['search_type'])

                    print(b"New Path: {}".format(new_path))

                    # Rename
                    if settings['is_prod']:
                        os.rename(work_path, new_path)

                print("=" * 20)

### Main ###
if __name__ == '__main__':
    MAIN_SCRIPT = FastRename()

    ### Arguments by search ###
    SEARCH_RULE = r'.*'                 # Search all files
    # REPLACE_RULE = r'[^0-9]*(\d*)'    # filename use first number only
    REPLACE_RULE = r'([\w\s]*)-.*'        # before dash only
    # REPLACE_RULE = r'.*?-([-\w\s]*)'    # after dash only
    ###-arguments ###

    MAIN_SCRIPT.rename(SEARCH_RULE,
                       REPLACE_RULE,
                       is_include_sub=True,
                       is_prod=False,
                       search_type="jpg")
