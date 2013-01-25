#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20130125
#  @date
#  @author        Chih-Yuan Chen
#  @brief         Settings and configuration for files_seeker.

# rules sample
check_newline = r'.*\r$'
check_space = r'.* $'
query_regx = r'.*foo.*'
rules = (check_newline, check_space, query_regx)

# search filename extension type
filename_extension = ('py', 'sample')

is_search_sub_dir = True
