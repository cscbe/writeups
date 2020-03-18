# Where in the Word is...

##  Created by Didier Stevens

## Description

While Carmen Sandiego can hide anywhere in the world, the flag you are looking for is just hiding in this Word document.

## Solution

The correct flag is stored in the compressed Dir stream (there are also some false flags, that can be extracted with strings: 

    CSC{ThisIsNotTheFlagAAAAAAAAAAAAAAAAAAAA}).

To extract the flag, select the Dir stream (index 9), decompress it (--decompress) and extract the strings (-S), like this:

 `oledump.py -s 9 --decompress -S Where_in_the_Word_is_....doc`

 