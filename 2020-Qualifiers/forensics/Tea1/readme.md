# Tea 1

## Challenge created by Remco Hofman

## Description
We managed to get limited access to a suspect's phone, can you see if we got anything useful from his 2FA app?

## Solution

The first thing you should probably do if you get a memory dump of a process is attempt to identify anything interesting in it's contents.  
`strings` is one of the first tools that come to mind:

`unzip dump.zip`  
`strings dump/* | uniq | tee dump_strings.txt`

This gives a lot of output, but `grep` is always at our disposal if we have some information about what we're looking for, like the flag format in this case:

`grep 'CSC{.*}' dump_strings.txt`

First flag found, easily: `CSC{TheCupOfHumanity...}`