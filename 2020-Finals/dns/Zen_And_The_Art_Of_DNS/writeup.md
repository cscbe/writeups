# IDEA 3 - “ZEN and the ART of DNS maintenance”

1. Info to start: https://www.zendns.be@886104891
  The decimal number behind @ is an IP decimal number which can be converted to IP address : 52.208.227.59 (https://www.ipaddressguide.com/ip)
  The domain zendns.be is the focus of this CTF (the weblink is misleading)
HINT: "Back on our trip out of Miles City you'll remember I talked about how formal scientific method could be applied to the repair of a 
motorcycle through the study of chains of cause and effect and the application of experimental method to determine these chains."
(quote from "Zen and the art of motorcycle maintenance"; which should give an indication to do DNS NSEC chain walking)

2.	Zone walk zendns.be (NSEC chain)

```sh
$ ldns-walk @localhost zendns.be
zendns.be.	zendns.be. NS SOA RRSIG NSEC DNSKEY TYPE65534
cogent.zendns.be. NAPTR RRSIG NSEC
dab.zendns.be. A RRSIG NSEC
dad.zendns.be. A RRSIG NSEC
daft.zendns.be. A RRSIG NSEC
dag.zendns.be. A RRSIG NSEC
daguerreotype.zendns.be. A RRSIG NSEC
dah.zendns.be. A RRSIG NSEC
…
survive.zendns.be. A RRSIG NSEC
suspect.zendns.be. A RRSIG NSEC
suspend.zendns.be. A RRSIG NSEC
sustain.zendns.be. A RRSIG NSEC
swallow.zendns.be. A RRSIG NSEC
swan.zendns.be. A RRSIG NSEC
swap.zendns.be. A RRSIG NSEC
sway.zendns.be. A RRSIG NSEC
swim.zendns.be. A RRSIG NSEC
sympathectomy.zendns.be. A RRSIG NSEC
sympatholytic.zendns.be. A RRSIG NSEC
symptom.zendns.be. A RRSIG NSEC
syn.zendns.be. A RRSIG NSEC
synchronicity.zendns.be. A RRSIG NSEC
syringomyelia.zendns.be. A RRSIG NSEC
universityofMaryland.zendns.be. NAPTR RRSIG NSEC
usarmyresearchlab.zendns.be. NAPTR RRSIG NSEC
verisign.zendns.be. NAPTR RRSIG NSEC
wideproject.zendns.be. NAPTR RRSIG NSEC
```

From the output, the special record NAPTR should be noticed
HINT: NAPTR is ART
(hint could also be added in the zone as a TXT record ?)

```sh
$ ldns-walk @localhost zendns.be | grep NAPTR
cogent.zendns.be. NAPTR RRSIG NSEC
dod.zendns.be. NAPTR RRSIG NSEC
icann.zendns.be. NAPTR RRSIG NSEC
isc.zendns.be. NAPTR RRSIG NSEC
isi.zendns.be. NAPTR RRSIG NSEC
nasa.zendns.be. NAPTR RRSIG NSEC
netnod.zendns.be. NAPTR RRSIG NSEC
ripencc.zendns.be. NAPTR RRSIG NSEC
universityofMaryland.zendns.be. NAPTR RRSIG NSEC
usarmyresearchlab.zendns.be. NAPTR RRSIG NSEC
verisign.zendns.be. NAPTR RRSIG NSEC
wideproject.zendns.be. NAPTR RRSIG NSEC
```
3.	Request all NAPTR records; these are the 12 operator’s (Verisign operates 2 root servers of the 13 DNS root servers
```sh
$ dig @localhost cogent.zendns.be NAPTR +short
16 2 "C" ".....nnnnnn.....nnnn.........." "!then!b!" .
29 3 "C" "....ssssssss.................." "!are!1!" .
3 1 "C" ".....ddddddddddddddd.........." "!reverse!7!" .

$ dig @localhost verisign.zendns.be NAPTR +short
27 3 "A" "........sssssssssss..........." "!flag!b!" .
10 1 "J" ".....dddd.......dddd.........." "!on!1!" .
23 2 "J" ".....nnnn.......nnnn.........." "!is!e!" .
14 2 "A" ".....nnnn.......nnnn.........." "!ns.zendns.be!5!" .
1 1 "A" ".....ddddddddddd.............." "!perform!3!" .
36 3 "J" "................ssss.........." "!next!!" .
```

4.	Order the output
Hint: www.root-servers.org
•	Put the D, N and S together and order by root server operator from A to M
Or the following fields also give an indication of ordering (this could be removed if this makes it too obvious ?)
•	The first column is the record number
•	The second column is either 1, 2 or 3 (same as D, N or S)
•	The third column indicates the root server character (A to M)
```sh
verisign.zendns.be. NAPTR 1 1 "A" ".....ddddddddddd.............." "!perform!3!" .
isi.zendns.be. NAPTR 2 1 "B" ".....ddddddddddddd............" "!DNS!a!" .
cogent.zendns.be. NAPTR 3 1 "C" ".....ddddddddddddddd.........." "!reverse!7!" .
universityofMaryland.zendns.be. NAPTR 4 1 "D" ".....dddd.......dddd.........." "!lookup!9!" .
nasa.zendns.be. NAPTR 5 1 "E" ".....dddd.......dddd.........." "!of!e!" .
isc.zendns.be. NAPTR 6 1 "F" ".....dddd.......dddd.........." "!the!f!" .
dod.zendns.be. NAPTR 7 1 "G" ".....dddd.......dddd.........." "!following!c!" .
usarmyresearchlab.zendns.be. NAPTR 8 1 "H" ".....dddd.......dddd.........." "!IPv6!b!" .
netnod.zendns.be. NAPTR 9 1 "I" ".....dddd.......dddd.........." "!address!a!" .
verisign.zendns.be. NAPTR 10 1 "J" ".....dddd.......dddd.........." "!on!1!" .
ripencc.zendns.be. NAPTR 11 1 "K" ".....ddddddddddddddd.........." "!DNS!2!" .
icann.zendns.be. NAPTR 12 1 "L" ".....ddddddddddddd............" "!name!3!" .
wideproject.zendns.be. NAPTR 13 1 "M" ".....ddddddddddd.............." "!server!7!" .

verisign.zendns.be. NAPTR 14 2 "A" ".....nnnn.......nnnn.........." "!ns.zendns.be!5!" .
isi.zendns.be. NAPTR 15 2 "B" ".....nnnn.......nnnn.........." "!and!c!" .
cogent.zendns.be. NAPTR 16 2 "C" ".....nnnnnn.....nnnn.........." "!then!b!" .
universityofMaryland.zendns.be. NAPTR 17 2 "D" ".....nnnn.nnn...nnnn.........." "!lookup!a!" .
nasa.zendns.be. NAPTR 18 2 "E" ".....nnnn...nnn.nnnn.........." "!the!e!" .
isc.zendns.be. NAPTR 19 2 "F" ".....nnnn.....nnnnnn.........." "!corresponding!7!" .
dod.zendns.be. NAPTR 20 2 "G" ".....nnnn.......nnnn.........." "!TXT!7!" .
usarmyresearchlab.zendns.be. NAPTR 21 2 "H" ".....nnnn.......nnnn.........." "!record!8!" .
netnod.zendns.be. NAPTR 22 2 "I" ".....nnnn.......nnnn.........." "!This!8!" .
verisign.zendns.be. NAPTR 23 2 "J" ".....nnnn.......nnnn.........." "!is!e!" .
ripencc.zendns.be. NAPTR 24 2 "K" ".....nnnn.......nnnn.........." "!THE!f!" .
icann.zendns.be. NAPTR 25 2 "L" ".....nnnn.......nnnn.........." "!Capture!4!" .
wideproject.zendns.be. NAPTR 26 2 "M" ".....nnnn.......nnnn.........." "!the!4!" .

verisign.zendns.be. NAPTR 27 3 "A" "........sssssssssss..........." "!flag!b!" .
isi.zendns.be. NAPTR 28 3 "B" "......sssssssssssss..........." "!you!a!" .
cogent.zendns.be. NAPTR 29 3 "C" "....ssssssss.................." "!are!1!" .
universityofMaryland.zendns.be. NAPTR 30 3 "D" "....ssss......................" "!looking!3!" .
nasa.zendns.be. NAPTR 31 3 "E" "....ssss......................" "!for!d!" .
isc.zendns.be. NAPTR 32 3 "F" ".......ssssss................." "!The!2!" .
dod.zendns.be. NAPTR 33 3 "G" "..........ssssss.............." "!IPv6!!" .
usarmyresearchlab.zendns.be. NAPTR 34 3 "H" "............ssssssss.........." "!address!!" .
netnod.zendns.be. NAPTR 35 3 "I" "................ssss.........." "!is!!" .
verisign.zendns.be. NAPTR 36 3 "J" "................ssss.........." "!next!!" .
ripencc.zendns.be. NAPTR 37 3 "K" ".........ssssssss............." "!to!!" .
icann.zendns.be. NAPTR 38 3 "L" ".....ssssssssss..............." "!this!!" .
wideproject.zendns.be. NAPTR 39 3 "M" ".....sssssssss................" "!text!!" .
```
5.	Strip off the first 5 fields and the ASCII art becomes clear
```sh
".....ddddddddddd.............." "!perform!3!" .
".....ddddddddddddd............" "!DNS!a!" .
".....ddddddddddddddd.........." "!reverse!7!" .
".....dddd.......dddd.........." "!lookup!9!" .
".....dddd.......dddd.........." "!of!e!" .
".....dddd.......dddd.........." "!the!f!" .
".....dddd.......dddd.........." "!following!c!" .
".....dddd.......dddd.........." "!IPv6!b!" .
".....dddd.......dddd.........." "!address!a!" .
".....dddd.......dddd.........." "!on!1!" .
".....ddddddddddddddd.........." "!DNS!2!" .
".....ddddddddddddd............" "!name!3!" .
".....ddddddddddd.............." "!server!7!" .

".....nnnn.......nnnn.........." "!ns.zendns.be!5!" .
".....nnnn.......nnnn.........." "!and!c!" .
".....nnnnnn.....nnnn.........." "!then!b!" .
".....nnnn.nnn...nnnn.........." "!lookup!a!" .
".....nnnn...nnn.nnnn.........." "!the!e!" .
".....nnnn.....nnnnnn.........." "!corresponding!7!" .
".....nnnn.......nnnn.........." "!TXT!7!" .
".....nnnn.......nnnn.........." "!record!8!" .
".....nnnn.......nnnn.........." "!This!8!" .
".....nnnn.......nnnn.........." "!is!e!" .
".....nnnn.......nnnn.........." "!THE!f!" .
".....nnnn.......nnnn.........." "!Capture!4!" .
".....nnnn.......nnnn.........." "!the!4!" .

"........sssssssssss..........." "!flag!b!" .
"......sssssssssssss..........." "!you!a!" .
"....ssssssss.................." "!are!1!" .
"....ssss......................" "!looking!3!" .
"....ssss......................" "!for!d!" .
".......ssssss................." "!The!2!" .
"..........ssssss.............." "!IPv6!!" .
"............ssssssss.........." "!address!!" .
"................ssss.........." "!is!!" .
"................ssss.........." "!next!!" .
".........ssssssss............." "!to!!" .
".....ssssssssss..............." "!this!!" .
".....sssssssss................" "!text!!" .
```

6.	Read the sentence from top to bottom:
“Perform DNS reverse lookup of the following IPv6 address on DNS name server ns1.zendns.be and then lookup the corresponding TXT record. This the THE Capture the flag you are looking for. The IPv6 address is next to this text”
(Instead could here already the CTF be included ?)
(The sentence can be adjusted if too obvious ?)

7.	Reverse lookup IPv6 address
$ dig @ns1.zendns.be -x 3a79:efcb:a123:75cb:ae77:88ef:44ba:13d2 +short
ctf33.zendns.be.

8.	Lookup corresponding TXT record
$ dig @ns1.zendns.be ctf33.zendns.be txt +short
"CSC{nAYGh2OxiEAYgjBq56zYFTKPy1d2h4uFDIOE26tJZ3Mw1dbsnN}"

9.	The CTF is : “nAYGh2OxiEAYgjBq56zYFTKPy1d2h4uFDIOE26tJZ3Mw1dbsnN”
NOTE: the zone has many ctf<nr>.zendns.be records

