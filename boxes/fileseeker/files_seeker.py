#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20110808
#  @date          20130125
#  @author        Chih-Yuan Chen
#  @brief         Visiting all directories and files to search keywords.

from __future__ import unicode_literals

import os
import re

import config

rules = config.rules
filename_extension = config.filename_extension
is_search_sub_dir = config.is_search_sub_dir

class Files_seeker:
    """
    @desc   Travel all directories and files

    @param  (Tuple) Filename Extension
            (Boolean) Visited sub directories?
    @return (List)  All paths found
    """
    def path_travel(self, search_type, is_include_sub=False):
        result_list = set()
        seek_type = '%s{1}' % ('|'.join(search_type))

        if is_include_sub:
            search_regx = re.compile(r"\.{0}(.*\.({1}))$".format(re.escape(os.sep), seek_type))
        else:
            search_regx = re.compile(r"\./([^{0}]*\.({1}))$".format(re.escape(os.sep), seek_type))

        for dirname, dirnames, filenames in os.walk('.'):
            for filename in filenames:
                tree_path = os.path.join(dirname, filename)
                path_result = search_regx.search(tree_path)

                if path_result:
                    result_list.add(path_result.group(1))

        return result_list

if __name__ == '__main__':
    my_seeker = Files_seeker()
    found_paths = set()

    result_paths = my_seeker.path_travel(filename_extension, is_search_sub_dir)

    total_file_count = 0
    found_file_count = 0

    # compile all rules
    regx_list = [re.compile(r, re.I) for r in rules]

    for file in result_paths:
        total_file_count += 1

        # ignore self file
        if file in (__file__, 'config.py'):
            continue

        with open(file, 'r') as open_file:

            line = open_file.readline()
            while line:
                # check all rules
                if any([rc.search(line) for rc in regx_list]):
                    found_file_count += 1
                    found_paths.add(file)
                    break

                line = open_file.readline()

            open_file.close()

    print("Total of all files: %s" % total_file_count)
    print("Total of found files: %s" % found_file_count)
    if total_file_count:
        rate = 100.0 * (total_file_count - found_file_count) / total_file_count
        print("Found rate: %.2f %%" % rate)
    print "================================="

    for file_path in found_paths:
        print(file_path)
