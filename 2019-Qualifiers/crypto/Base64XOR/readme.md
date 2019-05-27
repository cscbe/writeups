# Challenge
I found a way to thwart people breaking xor encryption! Instead of base64 encoding the encrypted message, I'll first encode the message before encrypting it. No more frequency analysis! Anyway, here is the method I used, It's so simple I'm surprised nobody thought about it before. Unbreakable!
`base64 -w 0 message.txt | xortool-xor -s <notthekey> -f - > message.enc`


# Solution

solution.py

```
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

```

```
base64 -w 0 message.txt | xortool-xor -s FzUvdewPTN8gkahU4Vs2Pwd -f - > message.enc

# get key back from this
python3 solution.py message.enc

xortool-xor -s FzUvdewPTN8gkahU4Vs2Pwd -f message.enc | base64 -d > message_decrypted.txt

```

Output:

```

The Project Gutenberg EBook of Moby Dick; or The Whale, by Herman
Melville

This eBook is for the use of anyone anywhere at no cost and with almost
no restrictions whatsoever.  You may copy it, give it away or re-use it
under the terms of the Project Gutenberg License included with this
eBook or online at www.gutenberg.org


Title: Moby Dick; or The Whale

Author: Herman Melville

Release Date: December 25, 2008 [EBook #2701] Last Updated: December 3,
2017

Language: English

Character set encoding: UTF-8


Okay, maybe it wasn't _that_ secure after all.
Flag: CSC{I_w0nd3r_how_DEFLATE_wouId_do}

*** START OF THIS PROJECT GUTENBERG EBOOK MOBY DICK; OR THE WHALE ***

```
