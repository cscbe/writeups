## The Ancient Writings #2

### Description


> When Mr. Blanche, the cleaning man, cleaned out the house of Dr XX he found another piece of paper containing a printout similar to the one of the easy challenge.
> You're again called in as you've proven yourself to be an expert in Medieval programming languages.
> Looking at the code you see that it must be an earlier version of the code.
> Unfortunately, one line is missing. Can you find this line ?

#### Technical

  - The final code will be assembled from three parts
    1. the first part of the code is "cscbe19_medium_pre.bf" 
    2. the second part (the missing line) has to be provided by you (more details below)
    3. the third part of the code is "cscbe19_medium_post.bf" 

  - This resulting final code will be run using the reference implementation interpreter for this language
  - The output of running the final code with the interpreter should be exactly the same as in the easy challenge (i.e. the flag of the easy challenge)
  - when the code genertates the correct output you will be awarded with ...

#### Your input

  - you have to submit "the second part" (2) discussed above
  - a single line, max 80 characters
  - all characters are in the Ascii range 0x20 - 0x7f
  - a newline (0x0a) will be added when to your input when assembling the final code
    1)
    2) + "\n"
    3)

  - your have to submit your your input to a webserver running at XX.YY.ZZ.WW on port 4242 at the URL /bef/medium/your_input_here

  So if you believe that the missing line is `  v *37 <   `  

  You would make the request
     http://XX.YY.ZZ.WW:4242/bef/medium/%20%20v%20*37%20%3C

### Solution

cscbe19_medium_pre.bf:
```
>232+*""43*52**5+65+:*4::**3:*21+:** "b"$                 v    >
^"78"v $  $ \ $ \ $<"x32P"    _                           "    v
^|%24<"SC{key_Y3ByZXNzZXk=}"  ^7        *:+33 +*27*7 *44"key"  <
<>47+:*1+                                     47+:*2+v    "   >^
```

cscbe19_medium_post.bf: 
```
>                                        >    34*9g"SC":vv     ^            
<                                                    v:,_@>"#_"^
>                                                    >  ^      <

0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZv^<>0123456789abcdefghijklmnopqrstuvwxyz
```

In order to get the same output as the Ancient Writings #1, the following line should be pasted between cscbe19_medium_pre.bf and cscbe19_medium_post.bf:

`                                         v           <`

This results in the following URL:

`/bef/medium/%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20v%20%20%20%20%20%20%20%20%20%20%20%3C"`


### Flag
`CSC{#d^wv<>e23$&@dDHC}`


### Creator
Kris Boulez
