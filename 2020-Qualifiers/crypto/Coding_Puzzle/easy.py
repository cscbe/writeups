#!/usr/bin/env python3

# Author: Wouter Coudenys

import re
import random
import base64
import sys

challenge_name = 'Letters'
the_flag = "CSC{4F8D5C87378A02EFF0B05B0BE107252B}"
abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

h = random.getrandbits(128)

def make(flag):

    # add md5s
    h1 = hex(random.getrandbits(128))[2:]
    h2 = hex(random.getrandbits(128))[2:]
    surrounded_flag = f'{h1}{flag}{h2}'

    # rev flag
    rev_flag = surrounded_flag[::-1]

    # rot 11
    rot11_flag = "".join([abc[(abc.find(c)+11)%26] if c in abc else c for c in rev_flag])

    # base64
    b64_flag = base64.b64encode(rot11_flag.encode()).decode()

    # remove =
    noequal_flag = b64_flag.replace('=', '')

    flag = noequal_flag
    return flag


def solve(flag):

    # add = (works with this size of flag)
    equal_flag = flag + '='

    # b64 decode
    b64_flag = base64.b64decode(equal_flag.encode()).decode()

    # rot 15
    rot15_flag = "".join([abc[(abc.find(c)+15)%26] if c in abc else c for c in b64_flag])

    # rev flag
    rev_flag = rot15_flag[::-1]

    # grep CSC{}
    flag = re.search(r'CSC\{.*\}', rev_flag).group()

    return flag



def usage():
    print('usage:')
    print(f'    {sys.argv[0]} solve|make [FLAG]')
    sys.exit(1)

if len(sys.argv[1:]) < 1:
    usage()

command = sys.argv[1]

if len(sys.argv[1:]) >= 2:
    flag = sys.argv[2]
else:
    flag = the_flag

if command in ('solve', 'make'):
    output = locals()[command](flag)
    print(output)
else:
    usage()




