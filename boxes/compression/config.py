#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20130124
#  @date
#  @brief         Settings and configuration for Compress.

# destination path
# ex. 'D:\100-Dropbox\Dropbox\Public' and 'D:\100-Dropbox\Dropbox\Sharing'
TARGET_PATH = r"D:\100-Dropbox\Dropbox"
TARGET_DIR = ('Public', 'Sharing')

# source path
# ex. 'D:\\99_SystemTools\2_Design\AppServ\www\mywiki\data\page'..
SOURCE_PATH = r"D:\99_SystemTools\2_Design\AppServ\www\mywiki\data"
SOURCE_DIR = ('pages', 'media')

# compress setting
COMPRESSION_MAIN = r"D:\99_SystemTools\7-Zip\7z.exe a -t7z"
DEFAULT_OUTPUT = 'pages'