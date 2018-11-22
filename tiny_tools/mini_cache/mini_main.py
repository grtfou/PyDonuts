import time
import random

from mini_cache import mini_cache


@mini_cache(10, debug=False)
def add(x, y):
    time.sleep(2)
    return x + y


for i in range(1, 10):
    print("Run {}: result {}".format(i, add(1, random.randint(1, 3))))
