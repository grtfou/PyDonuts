# -*- coding: utf-8 -*-
#  @date    160819 - Implated AES-ECB decoder and encoder
"""
AES decoder and encoder

Require Libraries:
(* is primary library)

pycrypto==2.6.1  # https://github.com/dlitz/pycrypto
"""
import base64

from Crypto.Cipher import AES

BLOCK_SIZE = 32


def aes_ecb_encode(raw, s_key):
    """
    AES encoder (ECB).

    Args:
        raw: (string) raw string
        s_key: (string) security key

    Returns:
        (string) encoding string
    """
    cipher = AES.new(s_key, AES.MODE_ECB)
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE
                         ) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

    return base64.b64encode(cipher.encrypt(pad(raw)))


def aes_ecb_decode(s_raw, s_key):
    """
    AES decoder (ECB).

    Args:
        raw: (string) encoding string by aes
        s_key: (string) security key

    Returns:
        (string) original string
    """
    cipher = AES.new(s_key, AES.MODE_ECB)
    unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    return unpad(cipher.decrypt(base64.b64decode(s_raw))).decode('utf-8')

if __name__ == '__main__':
    security_key = 'abcd' * 4
    raw = 'abcdefg12345'

    encoding_string = aes_ecb_encode(raw, security_key)
    print(encoding_string)

    decoding_string = aes_ecb_decode(encoding_string, security_key)
    print(raw, decoding_string)
    assert raw == decoding_string
