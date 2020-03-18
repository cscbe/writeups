# Lorem ipsum crypto

### Creator: Didier Stevens

## Description

During the cleanup of a small fire in the archives of our national intelligence service, the following document was found: lorem-ipsum-crypto.txt.

We don’t know to which file it belongs, but it was found on the shelves labelled “simple cryptography”.

It is your job to decode the message.

## Solution:

Only take into account the words, disregarding case.

Ignore the first 2 words: lorem ipsum.

The first 256 words are unique, and each represent a byte value: first word = byte value 0, second word = byte value 1, …

The words after these 256 encode the message. Look up the position of each word in the table of 256 words. This produces a byte value. Convert this byte value to an ASCII character. Do this for all remaining words.

Included is a Python program to do the decoding.

    c:\Python37\python.exe decode.py lorem-ipsum-crypto.txt

Output: This is the flag CSC{HDBJNDJZND}