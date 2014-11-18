#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20120821
#  @date          20141118 - Fixing bugs
"""
Search file to rename new filename
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import os
import re

class FastRename(object):
    '''
    File rename for regex
    '''

    def __init__(self):
        pass

    def __list_files(self, is_include_sub=False):
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
        is_prod = False
        is_include_sub = False
        search_type = "xml"

        for name, value in kwargs.items():
            if name == 'is_prod':
                is_prod = value
            elif name == 'is_include_sub':
                is_include_sub = value
            elif name == 'search_type':
                search_type = value

        ### travel path ###
        for work_path in self.__list_files(is_include_sub):
            # old file name and path
            dir_path = '{}{}'.format(os.sep.join(work_path.split(os.sep)[:-1]), os.sep)
            old_filename = work_path.split(os.sep)[-1]

            # Search rule
            find_rule = r"({})\.{}$".format(search_exp, search_type)
            find_file_path = re.search(find_rule, old_filename)

            if find_file_path:
                print("Old Path: {}".format(work_path))

                # Checking filename for replace new name
                new_name_set = re.search(replace_exp, find_file_path.group(1))

                if new_name_set:
                    new_path = '{}{}.{}'.format(dir_path, new_name_set.group(1), search_type)
                    new_path_no_ext = '{}{}'.format(dir_path, new_name_set.group(1))

                    # Avoid replace the same name file
                    if os.path.exists(new_path):
                        new_path_no_ext += "_1"
                        new_path = '{}.{}'.format(new_path_no_ext, search_type)

                    print("New Path: {}".format(new_path))

                    # Rename
                    if is_prod:
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
