# Where in the Word is …

##  Created by Wouter Coudenys

## Description
Employee is gone. The only thing he left behind was this paper on his desk with a few numbers on it. We tried to look at his hard drive, but all the bits look random. 

Piece of paper:
    26522
    26461
    64151
    16412
    32121
    55512

Given: chal.img

## Solution

Find the right words in http://world.std.com/%7Ereinhold/diceware.wordlist.asc
The words in the passphrase have spaces in between.
Then run:

    $ loop_device=$(losetup -f chal.img --show)
    $ crypsetup open $loop_device crypt
    $ mount /dev/mapper/crypt /mnt
    $ cat /mnt/flag.txt
    $ umount /mnt
    $ cryptsetup close crypt
    $ losetup -d $loop_device
