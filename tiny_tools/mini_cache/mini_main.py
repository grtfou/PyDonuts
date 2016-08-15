import time
from mini_cache import mini_cache

@mini_cache(10)
def main(x, y):
    time.sleep(2)
    return x + y

for i in range(1, 10):
    print("Run {}: {}".format(str(i), main(1, 2)))

