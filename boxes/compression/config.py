#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20130124
#  @date          20141107
'''
Settings and configuration for Compress
'''

# destination path
# ex. 'D:\100-Dropbox\Dropbox\Public'
#     'D:\100-Dropbox\Dropbox\Sharing'
TARGET_PATH = "D:\\100-Dropbox\\Dropbox"
TARGET_DIR = ('Public', 'com_sharing')

# source path
# ex. 'D:\\99_SystemTools\2_Design\AppServ\www\mywiki\data\page'..
SOURCE_PATH = "D:\\00-System-Tools\\2-Code\\DokuWikiStick\\dokuwiki\\data"
SOURCE_DIR = ('pages', 'media')

# compress setting
COMPRESSION_MAIN = "D:\\00-System-Tools\\0-Setup\\7-Zip\\7z.exe a -mhe -t7z"
OUTPUT_PREFIX_FILENAME = 'pages'
