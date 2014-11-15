#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20140620
#  @date          20140623 - Fixing bug
'''
XTEA for cryptography
Algorithm from (http://en.wikipedia.org/wiki/XTEA)
'''

import struct

class xtea:
    def __init__(self):
        pass

    ##
    #  @desc    Encoding(encrypt) string by key
    #  @param   (String) key (recommend 16 character (128 bits))
    #  @param   (String) for encrypt
    #  @param   (Integer) Cycle times (Feistel round loop) (recommend 32 times)
    #  @param   (String) endian for C compiler
    #  @return  (String) encrypt string
    def encrypt(self, key, data, run_times=32, end_str="!"):
        i = 0
        encrypt_str = ""

        ### data have to 8 multiple ###
        if len(data) % 8 != 0:
            data += chr(0) * (8 - (len(data) % 8))
        ###-
        ### key have to 16 multiple ###
        if len(key) % 16 != 0:
            key += chr(0) * (16 - (len(key) % 16))
        ###-

        while i < len(data):
            total_v = 0
            delta = 0x9e3779b9
            mask = 0xffffffff

            v0, v1 = struct.unpack("{}2L".format(end_str), data[i:i+8])
            k = struct.unpack("{}{}L".format(end_str, len(key) / 4), key)

            for round_time in range(run_times):
                v0 = (v0 + (((v1<<4 ^ v1>>5) + v1) ^ (total_v + k[total_v & 3]))) & mask
                total_v = (total_v + delta) & mask
                v1 = (v1 + (((v0<<4 ^ v0>>5) + v0) ^ (total_v + k[total_v>>11 & 3]))) & mask

            encrypt_str += struct.pack("{}2L".format(end_str), v0, v1)
            i += 8

        return encrypt_str

    ##
    #  @desc    Decoding(encrypt) string by key
    #  @param   (String) key (recommend 16 character (128 bits))
    #  @param   (String) for encrypt
    #  @param   (Integer) Cycle times (Feistel round loop) (recommend 32 times)
    #  @param   (String) endian for C compiler
    #  @return  (String) decrypt string
    def decrypt(self, key, data, run_times=32, end_str="!"):
        i = 0
        decrypt_str = ""

        ### key have to 16 multiple ###
        if len(key) % 16 != 0:
            key += chr(0) * (16 - (len(key) % 16))
        ###-

        while i < len(data):
            total_v = 0
            delta = 0x9e3779b9
            mask = 0xffffffff

            # struct.pack / unpack : string to bit
            v0, v1 = struct.unpack("{}2L".format(end_str), data[i:i+8])
            k = struct.unpack("{}{}L".format(end_str, len(key) / 4), key)

            total_v = (delta * run_times) & mask
            for round_time in range(run_times):
                v1 = (v1 - (((v0<<4 ^ v0>>5) + v0) ^ (total_v + k[total_v>>11 & 3]))) & mask
                total_v = (total_v - delta) & mask
                v0 = (v0 - (((v1<<4 ^ v1>>5) + v1) ^ (total_v + k[total_v & 3]))) & mask

            decrypt_str += struct.pack("{}2L".format(end_str), v0, v1)
            i += 8

        return decrypt_str.rstrip(chr(0))

def test(run_times):
    data = 'Hello World and My Friend!!'
    key = 'ABCDEFGH' * 2

    x = xtea()
    encoding_code = x.encrypt(key, data, run_times)
    x.decrypt(key, encoding_code, run_times)

if __name__ == '__main__':
    data = 'Hello World and My Friend!!'
    key = 'ABCDEFGH' * 2
    run_times = 2
    x = xtea()

    encoding_code = x.encrypt(key, data, run_times)
    decoding_code = x.decrypt(key, encoding_code, run_times)

    print(len(data), "Original String: {}".format(data))
    print(len(decoding_code), "Decoding String: {}".format(decoding_code))
    print(data == decoding_code)
    print(len(key), "Key: {}".format(key))
    print(len(encoding_code), 'hash code: {}'.format(encoding_code.encode('hex')))
    print('='*20)

    ### test 1000 times ###
    import timeit
    t = timeit.Timer("test(run_times=2)", "from __main__ import test")
    print('Test time: {} sec/time'.format(t.timeit(number=1000)))