#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20120821
#  @date          20141107
"""
Search file to rename new filename
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import os
import re

class FastRename:
    def __init__(self):
        pass

    def __list_files(self, is_include_sub=False):
        search_file_list = []
        for dirname, _, filenames in os.walk(os.getcwd()):
            for filename in filenames:
                tree_path = os.path.join(dirname, filename)
                search_file_list.append(tree_path)

            if not is_include_sub:
                return search_file_list

        return search_file_list

    def rename(self, search_exp, replace_exp, is_include_sub=False, is_prod=True, search_type="xml"):
        work_file_list = []

        for work_path in self.__list_files(is_include_sub):
            find_file_path = re.search(r".*\\({})\.{}$".format(search_exp, search_type),
                                       work_path)

            if find_file_path:
                print("Old Path Name: {}".format(work_path))

                new_name_set = re.search(r'(.*\\){}'.format(replace_exp), work_path)

                prefix_name = new_name_set.group(1)
                suffix_name = new_name_set.group(2)

                if new_name_set and prefix_name and suffix_name:
                    new_file_name = '{}{}.jpg'.format(prefix_name, suffix_name)
                    print("New Path Name: {}".format(new_file_name))

                    # Rename
                    if is_prod:
                        os.rename(work_path, new_file_name)

                print("=" * 20)

                work_file_list.append(work_path)

        return work_file_list

### Main ###
if __name__ == '__main__':
    my_script = FastRename()

    ### Arguments by search ###
    search_exp = r'.*'   # Search all files

    replace_exp = r'[^0-9]*(\d*)'  # filename use first number only
    # replace_exp = r'([\w ]*)-.*'   # before dash only
    # replace_exp = r'.*?-([-\w ]*)' # after dash only
    ###-arguments ###

    my_script.rename(search_exp,
                     replace_exp,
                     is_include_sub=False,
                     is_prod=False,
                     search_type="jpg")
