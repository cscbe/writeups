#!/bin/bash
set -e

# Author: Wouter Coudenys
# challenge_name = 'Roll the dice'

# ###########################################
# Hint: Picture of dice.
# Description: Employee is gone. The only
# thing he left behind was this paper on his 
# desk with a few numbers on it.
# We tried to look at his hard drive, but
# all the bits look random.
# Piece of paper:
#   26522
#   26461
#   64151
#   16412
#   32121
#   55512
# ###########################################

passphrase="gab fuss whop chase guide stem"
flag=${1:-CSC{38d38daa807eeb95e87f8a2344dd9c98}}

modprobe loop
dd if=/dev/urandom of=randombits count=5 bs=10M
loop_device=$(losetup -f randombits --show)

echo -n $passphrase | cryptsetup luksFormat $loop_device -

echo -n $passphrase | cryptsetup open --key-file - $loop_device crypt
mkfs -t ext4 /dev/mapper/crypt
mount /dev/mapper/crypt /mnt

echo $flag > /mnt/flag.txt

umount /mnt
cryptsetup close crypt
losetup -d $loop_device

mv randombits chal.img
echo
echo challenge file created: chal.img

# ###########################################
# Solution:
# Find the right words in 
# http://world.std.com/%7Ereinhold/diceware.wordlist.asc
# The words in the passphrase have spaces in between.
# Then run:
# $ loop_device=$(losetup -f chal.img --show)
# $ crypsetup open $loop_device crypt
# $ mount /dev/mapper/crypt /mnt
# $ cat /mnt/flag.txt
# $ umount /mnt
# $ cryptsetup close crypt
# $ losetup -d $loop_device
# ###########################################
