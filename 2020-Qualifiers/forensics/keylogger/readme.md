# Where in the Word is ...

##  Created by Didier Stevens

## Description
Ok, now I lost all hope... Our last standing server just got breached. As a last call, I was able to dump the memory of a keylogger and I even reverse engineered the source code! Could you please find out what they stole?

## Solution
csc-keylogger.exe_200212_200703.dmp is the process memory dump (procdump.exe -mp) of a running C program (Windows, .exe) that is a keylogger.
The memory dump contains a a buffer with keyboard scancodes that were taken on a computer where I was typing. I type the flag on that computer.

Extracting the flag is hard, and I suggest to include file csc-keylogger.cpp with the challenge, so that students can better understand how to parse the memory dump.

The C++ program contains a struct.

    struct KEYBOARDBUFFER {
        char szMarker [32];
        HKL sKeyboardLayout;
        int iCounter;
        unsigned char aucBuffer[10240];
    } sKEYBOARDBUFFER;

The marker (szMarker) is set to `<<<KEYBOARD_BUFFER>>>`
Search for that marker in the memory dump, and then you found the start of the structure in memory.
It's a buffer with keyboard scancodes (Belgian keyboard, this info can be derived from field sKeyboardLayout in the struct.
There are 120 scancodes in the buffer (field iCounter)

I also wrote a Python script that parses the keyboard buffer and displays the flag: csc-keylogger.py

Using it is simple:

    csc-keylogger.py csc-keylogger.exe_200212_200703.dmp

