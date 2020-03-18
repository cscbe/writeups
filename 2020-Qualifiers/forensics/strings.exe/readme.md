# Where in the Word is …

##  Created by Didier Stevens

## Description
We found a weird program running on one of our servers and created a memory dump. Can you figure out what it does?

## Solution
csc-strings.exe_200213_232412.dmp is the process memory dump (procdump.exe -mp) of a running C program (Windows, .exe) containing a bunch of random strings that resemble a flag and on valid vlag.

Extracting the flag is simple:

    strings csc-strings.exe_200213_232412.dmp | grep CSC | head
Output:

> This is not the flag: CSC{ThisIsNotTheFlagEzjQn} This is not the
> flag: CSC{ThisIsNotTheFlagmQ%9&,q0Rcm5{} This is not the flag:
> CSC{ThisIsNotTheFlag'Z'@D!UH@} This is not the flag:
> CSC{ThisIsNotTheFlagNK`Y1o>.-]c} This is not the flag:
> CSC{ThisIsNotTheFlag#)D0Fw~} This is not the flag:
> CSC{ThisIsNotTheFlagmwBnSj2} This is not the flag:
> CSC{ThisIsNotTheFlagzWE#v/,jFvW} This is not the flag:
> CSC{ThisIsNotTheFlagoRW{D} This is not the flag:
> CSC{ThisIsNotTheFlagA[sQ$I\:} This is not the flag:
> CSC{ThisIsNotTheFlag]xBL52;d_wB}

    strings csc-strings.exe_200213_232412.dmp | grep -v ThisIsNot | grep CSC

This is ... the flag: **CSC{Gdpvbetaocd53hf}cdjce90xs}**



