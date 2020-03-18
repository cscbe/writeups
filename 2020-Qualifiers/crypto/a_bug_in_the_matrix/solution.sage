#!/usr/bin/sage

# Run `PWNLIB_NOTERM=true sage solution.sage` if curses crash

from pwn import *
from Crypto.Util.number import *
import progressbar
#context.log_level = 'debug'

GF2 = GF(2)
blockSize = int(512)

conn = remote("54.72.64.138", 1337)

conn.recvline()
def getEncryptedLine(conn):
    return vector(GF2, [int(y) for y in ('{0:0'+str(blockSize)+'b}').format(int(conn.recvline().strip(), 16))])

encFlag = getEncryptedLine(conn)

conn.recvline()
conn.sendline('0')
offset = getEncryptedLine(conn)

vectors = []
print("Constructing ciphertext basis")
for i in range(blockSize):
    conn.recvline()

    conn.sendline(('{0:0'+str(blockSize/4)+'x}').format(int('1' + '0' * (blockSize - i - int(1)), 2)))
    vectors += [ getEncryptedLine(conn) - offset ]

print("Solving linear equation")
# Solving linear equation
m = matrix(GF2, vectors).transpose()
plaintext = m.solve_right(encFlag - offset)

# Transform bitvector to flag
plaintext = ''.join(map(str, plaintext))
plaintext = long_to_bytes(int(plaintext, 2))
print(plaintext)


