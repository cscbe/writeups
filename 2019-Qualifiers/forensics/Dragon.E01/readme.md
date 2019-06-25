## Dragon.EO1

### Description

> We discovered a rogue device in our datacenter, our forensics team already created an image but can't seem to find the secret. Can you help?

### Solution

The challenge can either be solved on Windows or Linux

#### Windows

Mount the image using ftk imager or ewf viewer.

[https://github.com/cscbe/writeups/tree/master/2019-Qualifiers/forensics/Dragon.E01/img/img1.png]]

Just by looking closely to the file you'll find the flag

[https://github.com/cscbe/writeups/tree/master/2019-Qualifiers/forensics/Dragon.E01/img/img2.png]]

Or you mount the image using the dir /r on the new drive will reveal the alternative data stream

[https://github.com/cscbe/writeups/tree/master/2019-Qualifiers/forensics/Dragon.E01/img/img3.png]]

Using any "text utilities" to open the file will display the flag

[https://github.com/cscbe/writeups/tree/master/2019-Qualifiers/forensics/Dragon.E01/img/img4.png]]

Powershell:
`gci -recurse | % { gi $_.FullName -stream * } | where stream -ne ':$Data'`

[https://github.com/cscbe/writeups/tree/master/2019-Qualifiers/forensics/Dragon.E01/img/img5.png]]

[https://github.com/cscbe/writeups/tree/master/2019-Qualifiers/forensics/Dragon.E01/img/img6.png]]



#### Linux

Mount the image using ewfinfo and ewfmount

[https://github.com/cscbe/writeups/tree/master/2019-Qualifiers/forensics/Dragon.E01/img/img7.png]]

[https://github.com/cscbe/writeups/tree/master/2019-Qualifiers/forensics/Dragon.E01/img/img8.png]]


Mount the image to /mnt in ntfs

[https://github.com/cscbe/writeups/tree/master/2019-Qualifiers/forensics/Dragon.E01/img/img9.png]]


Find Alternative datastream 

[https://github.com/cscbe/writeups/tree/master/2019-Qualifiers/forensics/Dragon.E01/img/img10.png]]



### Flag
`CSC{!Dr@g0N_Rul35!}`


### Creator
Sébastien de Tillesse


