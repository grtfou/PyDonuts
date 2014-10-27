import time
import string
import random

def get_random_pwd(length=32):
    hash_str = '{{0:0{}x}}'.format(length)
    return hash_str.format(random.randrange(16**length))

def get_random_str(length=20):
    hash_choice = string.digits + string.ascii_letters
    return ''.join([random.choice(hash_choice) for x in range(length)])


if __name__ == '__main__':
    print(get_random_pwd())
    print(get_random_str())

    time.sleep(10)
