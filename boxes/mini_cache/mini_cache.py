#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20140807
#  @date          20140811
#  @version       1.0
"""
mini cache
"""
import inspect
import time

### limit the memory ###
''' 限制cache最多用多少記憶體
    目前下面的程式是 限制全部程式(含import的程式)，所以不好用
    1048576L = 2的20次方 = 1048516 bytes = 1048.516K = 1 MB

# import resource
# megs = 5
# resource.setrlimit(resource.RLIMIT_AS, (megs * 1048576L, -1L))
# print("usage stats", "=>", resource.getrusage(resource.RUSAGE_SELF))
#-
'''

# key: program + function
# value: stored time
#        function result (by function return)
__cache = {}

##
# TODO: 1. 優先序 (太久沒被讀的cache被替換掉)
#          或者 先換掉最舊的cache (最多記多少筆cache)
#       2. 轉換: 可以改設成存成檔案(I/O)
def mini_cache(expired_time=3600, stored_engine='cache'):
    """
    Args:
        expired_time: (int) second of expired function result
    """

    def __set_env(myfunc):
        """
        Args:
            myfunc: (function object) main execution function
        """
        # program path for key of cache naming
        target_path = inspect.getsourcefile(myfunc)

        def __set_cache(*args, **kwargs):
            """
            Args:
                *args, **kwargs: main execution function arguments
            """
            global __cache
            key = "{},{}:{},{}".format(target_path, myfunc.func_name,
                                       args, kwargs)
            if key in __cache.keys():
                print('find')
                now = time.time()
                if (expired_time > 0) and (now - __cache[key][0] < expired_time):
                    return __cache[key][1]

            __cache[key] = [time.time(),
                            myfunc(*args, **kwargs)]

            print("cache: {}".format(str(__cache)))
            return __cache[key][1]

        return __set_cache

    return __set_env
