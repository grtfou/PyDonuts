#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20120821
#  @date          20141125 - Fixing encoding issue
"""
Search file to rename new filename
"""
from __future__ import unicode_literals
from __future__ import print_function

import os
import re
import random
import sys

CMD_ENCODE = sys.stdout.encoding

class VisitPath(object):
    '''
    Get all file path
    '''

    @classmethod
    def list_files(cls, is_include_sub=False):
        '''
        Visit file(folder) path by regex
        '''
        search_file_list = []
        for dirname, _, filenames in os.walk(u'{}'.format(os.getcwd())):
            for filename in filenames:
                tree_path = os.path.join(dirname, filename)
                search_file_list.append(tree_path)

            if not is_include_sub:
                return search_file_list

        return search_file_list

class FastRename(object):
    '''
    File rename for regex
    '''

    @classmethod
    def rename(cls, search_exp, replace_exp, **kwargs):
        '''
        Main function for rename the file
        '''
        settings = {'is_prod': False,
                    'source_paths': [''],
                    'search_type': "xml"}

        for name, value in kwargs.items():
            settings[name] = value

        ### travel path ###
        for work_path in settings['source_paths']:
            # old file name and path
            dir_path = r'{}{}'.format(os.sep.join(work_path.split(os.sep)[:-1]),
                                      os.sep)

            # Search rule
            find_rule = r"({})\.{}".format(search_exp, settings['search_type'])
            find_file_path = re.search(find_rule, work_path.split(os.sep)[-1],
                                       re.UNICODE)

            if find_file_path:
                print("Old Path: {}".format(work_path.encode(CMD_ENCODE,
                                            "replace").decode(CMD_ENCODE)))

                # Checking filename for replace new name
                new_name_set = re.search(replace_exp, find_file_path.group(1),
                                         re.UNICODE)

                if new_name_set:
                    new_path = r'{}{}.{}'.format(dir_path,
                                                new_name_set.group(1),
                                                settings['search_type'])
                    new_path_no_ext = r'{}{}'.format(dir_path,
                                                     new_name_set.group(1))

                    # Avoid replace the same name file
                    if os.path.exists(new_path):
                        new_path = r'{}_{}.{}'.format(new_path_no_ext,
                                                     str(random.randint(1, 99)),
                                                     settings['search_type'])

                    print("New Path: {}".format(new_path.encode(CMD_ENCODE,
                                                "replace").decode(CMD_ENCODE)))

                    # Rename
                    if settings['is_prod']:
                        os.rename(work_path, new_path)

                print("=" * 20)

### Main ###
if __name__ == '__main__':
    SOURCE_PATH = VisitPath().list_files(is_include_sub=True)

    ### Arguments by search ###
    SEARCH_RULE = r".*"                 # Search all files
    # REPLACE_RULE = r'[^0-9]*(\d*)'    # filename use first number only
    REPLACE_RULE = r'([\w\s]*)-.*'        # before dash only
    # REPLACE_RULE = r'.*?-([-\w\s]*)'    # after dash only
    ###-arguments ###

    IS_PROD = True if len(sys.argv) > 1 and sys.argv[1] == 'run' else False

    FastRename().rename(SEARCH_RULE,
                        REPLACE_RULE,
                        source_paths=SOURCE_PATH,
                        is_prod=IS_PROD,
                        search_type="txt")
