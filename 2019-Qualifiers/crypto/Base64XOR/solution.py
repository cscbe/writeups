#!/usr/bin/env python3
# Made for NVISO by Thomas De Backer

from collections import Counter
import math
import sys

CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789="

MOSTFREQ = (b'IHRo', b'dGhl', b'aGUg', b'ZWQg', b'IAoK')

txt_xor = open(sys.argv[1], "rb").read()


def bxor(b1, b2):
    result = bytearray()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return result


def collect_pairs(t, kl, off=0):
    count = Counter([t[kl*i+off:kl*i+4+off] for i in range(len(t)//kl)])
    return count


def try_keylength(klo):
    completekey = ""
    kl = 4*klo//math.gcd(4, klo)
    for k_offset in range(0, kl, 4):
        topp = collect_pairs(txt_xor, kl, k_offset).most_common(100)

        # guess key
        for w, (v, _) in zip(MOSTFREQ, topp[:5]):
            key = bxor(w, v)
            guess = [bxor(i, key).decode() for i, _ in topp]
            if all(k in CHARS for c in guess for k in c):
                completekey += key.decode()
                break
        else:
            return "no key found"
    return "possible key: {}".format(completekey[:klo])


for i in range(3, 35):
    print("Trying keylength", i, end=": ")
    print(try_keylength(i))
