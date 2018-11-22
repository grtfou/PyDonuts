"""
mini cache
  @first_date    140807
  @date          181122
  @TODO:         record limit (the oldest record will be replaced)
"""
import inspect
import time


"""
  * key: program filename + function name
  * value: created time, function result
"""
__cache = {}


def mini_cache(expired_time=3600, debug=False):
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
        filename = inspect.getsourcefile(myfunc)

        def __set_cache(*args, **kwargs):
            """
            Args:
                *args, **kwargs: main execution function arguments
            """
            global __cache
            key = "{},{}:{},{}".format(filename, myfunc.__name__,
                                       args, kwargs)
            if key in __cache.keys():
                if debug:
                    print('find it (in memory)')
                now = time.time()
                if (expired_time > 0) and (
                   now - __cache[key][0] < expired_time):

                    return __cache[key][1]
            else:
                if debug:
                    print('not found')

            __cache[key] = [int(time.time()),
                            myfunc(*args, **kwargs)]

            if debug:
                print("cache: {}".format(str(__cache)))
            return __cache[key][1]

        return __set_cache

    return __set_env
