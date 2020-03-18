# IDEA 2 - “Fake news!”

You can try to check if https://youtu.be is really hacked, but I wouldn’t waste my time on that.

1.	Check the forensics.reg Windows registry extract. There you will find the stub resolvers that return this false information.
```css
[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\services\Tcpip\Parameters\Interfaces\{E1D69A76-8615-45F2-B659-5E12F955DEEA}]
"UseZeroBroadcast"=dword:00000000
"EnableDeadGWDetect"=dword:00000001
"EnableDHCP"=dword:00000001
"NameServer"="54.154.165.103,127.0.0.2"
"Domain"=""
"RegistrationEnabled"=dword:00000000
"RegisterAdapterName"=dword:00000000
"DhcpIPAddress"="0.0.0.0"
"DhcpSubnetMask"="255.0.0.0"
"DhcpServer"="255.255.255.255"
"Lease"=dword:00000000
"LeaseObtainedTime"=dword:00000000
"T1"=dword:00000000
"T2"=dword:00000000
"LeaseTerminatesTime"=dword:00000000
"AddressType"=dword:00000000
"IsServerNapAware"=dword:00000000
"DhcpConnForceBroadcastFlag"=dword:00000000
```
2.	Let’s check that name server running on 54.154.165.103. 
```css
$ dig @54.154.165.103 youtu.be 

;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 41166
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available
```
The authoritative answer (AA) bit is set.
Which is weird, because if you try:
```css
dig youtu.be

;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 7567
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 4, ADDITIONAL: 9

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;youtu.be.			IN	A

;; ANSWER SECTION:
youtu.be.		24	IN	A	216.58.211.110

;; AUTHORITY SECTION:
youtu.be.		86124	IN	NS	ns3.google.com.
youtu.be.		86124	IN	NS	ns2.google.com.
youtu.be.		86124	IN	NS	ns1.google.com.
youtu.be.		86124	IN	NS	ns4.google.com.

;; ADDITIONAL SECTION:
ns3.google.com.		12813	IN	A	216.239.36.10
ns1.google.com.		12813	IN	A	216.239.32.10
ns4.google.com.		12813	IN	A	216.239.38.10
ns2.google.com.		12813	IN	A	216.239.34.10
ns3.google.com.		12813	IN	AAAA	2001:4860:4802:36::a
ns1.google.com.		12813	IN	AAAA	2001:4860:4802:32::a
ns4.google.com.		12813	IN	AAAA	2001:4860:4802:38::a
ns2.google.com.		12813	   IN	 AAAA	2001:4860:4802:34::a
```
The name server in the network interface configuration on the Windows host clearly is a lying DNS server.

3.	So, now we know that. But is that a dead end? Maybe better to first analyse the screenshot.
Download the screenshot and examine the file HackEd_Scr.jpg.
There is an essential hint hidden in the metadata.
Use exiftool or another suitable tool.
```css
$ exiftool -a -u -gl HackEd_Scr.jpg
```
You will find the hint in the XMP Location:
```css
XMP Location: https://hostname+version
```

4.	It seems that you need to find out a specific hostname and a version to compose a new URL.
```css
$ dig @54.154.165.103 hostname.bind chaos txt +short
;; ANSWER SECTION:
Hostname.bind.		60 	CH 	TXT 	"geppetto.devnull"
```

Mmmmh, devnull. That’s not really an existing top-level domain. 
```css
$ dig @54.154.165.103 geppetto.devnull
;; ANSWER SECTION:
geppetto.devnull 3600 IN CNAME youtu.be
```
Ok, we are back where we started; youtu.be. So that’s the host we are looking for.
Now we still need to find out the version.
```css
$ dig @54.154.165.103 version.bind chaos txt +short
;; ANSWER SECTION:
version.bind. 0 CH TXT "3Gh4Z3GT-R8"
```

That makes: https://youtu.be/3Gh4Z3GT-R8

5.	If you copy+paste that in a regular browser, you will see an animated movie. After a while, a QR code is displayed. When you scan that code, you will see the flag.
QR code: ![Alt](/qrcode.jpeg "QR")
 

The CTF is: CSC{DNSSEC4ever}





