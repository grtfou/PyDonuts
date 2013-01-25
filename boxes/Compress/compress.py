#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20110902
#  @date          20130124
#  @author        Chih-Yuan Chen
#  @brief         This program can copy, packing files(directions) to another target place.

from __future__ import unicode_literals

import sys
import os
import datetime
import time

import config

SOURCE_PATH = os.path.abspath(config.SOURCE_PATH)
SOURCE_DIR = config.SOURCE_DIR

TARGET_PATH = os.path.abspath(config.TARGET_PATH)
TARGET_DIR = config.TARGET_DIR

COMPRESSED_MAIN = os.path.abspath(config.COMPRESSED_MAIN)
DEFAULT_OUTPUT = config.DEFAULT_OUTPUT

"""
    @desc   Compressed files/directories by compressed format.

    @param  (Tuple) Waiting to compress files/directories absoulte path
            (String) Output absolute path
"""
def compressed(input, output, type):
    type = type.lower()
    if type == 'gzip':
        import tarfile

        tar = tarfile.open("%s.tar.gz" % output, "w:gz")
        for source in input:
            tar.add(source, arcname=source.split(os.sep)[-1])

        tar.close()
    elif type == '7zip':
        cmd = "{0} \"{1}\" {2}".format(COMPRESSED_MAIN, output, " ".join(input))
        os.system(cmd)
    else:
        print("No found this compressed type.")

def main(type, output):
    today = datetime.datetime.now().strftime('%y-%m-%d')

    for output_dir in TARGET_DIR:
        append_path = []
        for backup_folder in SOURCE_DIR:
            input = os.path.join(SOURCE_PATH, backup_folder)
            append_path.append(input)

        output_path = os.path.join(TARGET_PATH, output_dir,
                                   "%s(%s)" % (output, today))

        compressed(append_path, output_path, type)

        time.sleep(2)

if __name__ == '__main__':
    """
    Get options
    """
    if len(sys.argv) > 2:
        compression_output = sys.argv[2]
    else:
        compression_output = DEFAULT_OUTPUT

    if len(sys.argv) > 1:
        compression_type = sys.argv[1]
    else:
        compression_type = '7zip'

    main(compression_type, compression_output)


