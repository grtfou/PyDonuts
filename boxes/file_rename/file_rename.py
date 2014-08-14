# -*- coding: utf-8 -*-
#  @first_date    20120821
#  @date
#  @author        Chihyuan
#  @version       - 1.0 [public release]
#
#  @brief         This program can search file to rename new file name.

import os
import re

class FastRename:
    def list_files(self, is_include_sub=False):
        search_file_list = []
        for dirname, dirnames, filenames in os.walk(os.getcwd()):
            for filename in filenames:
                tree_path = os.path.join(dirname, filename)
                search_file_list.append(tree_path)

            if not(is_include_sub):
                return search_file_list

        return search_file_list

    def rename(self, path_list, search_type="xml"):
        work_file_list = []

        for work_path in path_list:
            find_file_path = re.search(r'.*\\(' + search_exp + ')\.' + search_type.lower() + '$', work_path)

            if find_file_path:
                print "Old Path Name: %s" % (work_path)

                new_name_set = re.search(replace_exp, work_path)
                # print(new_name_set, new_name_set.group(1), new_name_set.group(2))
                if new_name_set and new_name_set.group(1) and new_name_set.group(2):
                    new_file_name = new_name_set.group(1) + new_name_set.group(2) + '.jpg' # + search_type.lower()
                    print "New Path Name: %s" % (new_file_name)

                    # Rename
                    os.rename(work_path, new_file_name)

                print "===================="

                work_file_list.append(work_path)

        return work_file_list

### Main ###
if __name__ == '__main__':
    my_exe = FastRename()
    files_list = []

    ### Arguments by search ###
    search_exp = '.*'   # Search all files
    #replace_exp = r'(.*\\)[^0-9]*(\d*)' # 檔名只取第一組數字
    #replace_exp = r'(.*\\)([\w ]*)-.*' # 減號後面不要
    # replace_exp = r'(.*\\).*?-([-\w ]*)' # 第一個減號前面不要
    replace_exp = r'(.*\\)([0-9]+).*' # 第一個減號前面不要
    ###-arguments ###

    # Execute .txt and .sample files
    my_list = my_exe.list_files(False)

    # files_list.extend(my_exe.rename(my_list, "txt"))
    # files_list.extend(my_exe.rename(my_list, "jpg"))
    files_list.extend(my_exe.rename(my_list, "!ut"))

    # All find files path
    # for find_path in files_list:
    #     print find_path