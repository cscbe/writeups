# The blind

## Description
I wrote the password of my Wi-Fi network in this text file to never forget it again.
But after I gave it to this blind guy, everything was gone! The blind guy laughed at me and said "See, isn't it fun to not be able to see?".

Could you help me retrieve the password?

## Solution
The challenge is fairly easy and straightforward. The "Sight Deception.txt" contains a WhiteSpace program.
The contenders only have to figure out that the file is actually nto empty and figure out that it is a program.

The flag is obtain by just running the program and is the following:

`CSC{1_aM_c0mpl3t3ly_bl1nd}`

The assembly equivalent code is the following:

 push 0
 push 125
 push 100
 push 110
 push 49
 push 108
 push 98
 push 95
 push 121
 push 108
 push 51
 push 116
 push 51
 push 108
 push 112
 push 109
 push 48
 push 99
 push 95
 push 77
 push 97
 push 95
 push 49
 push 123
 push 67
 push 83
 push 67

label_0:
 dup
 jz label_1
 printc
 jmp label_0

label_1:
 end

