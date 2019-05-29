## Hacker C4TZ

### Description

> Our 60 year old sysadmin has just received this e-mail. Can you help him?

> From: hacker-c4tz@cyber-demon.doom
> To: admin@localhost
> Subject: Your website = Mine!
> Hello there! I've hacked your precious website! It wasn't that hard! Just soms reverse recognition on the SSL firewall database handler proxy, bundled with an AES triple 2048 Pro++!
> If you want your precious site back! Send me the five flags distributed across your website, to show you are worth having one!
> 
> Kind regards,
> H4CK3R C4TZ
> Challenge location: http://tl0.be/

### Solution


This challenge consists of five parts. This section describes the information about the challenge in general.
The description of the challenge explains that five flags are distributed to bring a website back online, after a hack executed by someone who loves cats.
The website is accesible on TL0.BE, and shows a simple website with an animated GIF. Upon investigating of the source code, there is no IMG tag, but there are some Javascript libraries embedded... And thus the search begins.
*Note! There is no need to exploit a service on this website.*
For these challenges, no specific tools have to be installed on your computer, sometimes, an online service, or a web browser, can already do miracles!

#### Challenge 1

The first flag is hidden inside the HTTP header, and can easily be read using curl...
```
$ curl -i http://tl0.be/
HTTP/1.1 200 OK
X-Powered-By: Express
X-Flag: CSC{01-TastyHeaderForBreakfast}
Accept-Ranges: bytes
Cache-Control: public, max-age=0
(...)
```
The flag is therefore CSC{01-TastyHeaderForBreakfast}.


#### Challenge 2

The second flag is hidden inside the Javascript libraries on the front page of the website. There are two scripts included:

```
<script type="text/javascript" src="js/jquery-3.3.1.min.js"></script>
<script type="text/javascript" src="js/index.js"></script>
```

The first one seems to be a download of jQuery 3.3.1 (minified), and the second one is a custom- written Javascript file that has been obfuscated. Upon investigation, this file will not contain any flag. The flag has been hidden inside the source code of the minified jQuery. Grepping (or CTRL+F) in that file will result in the following key...

```
(...) ipt, application/x-ecmascript"},flag:"CSC{02-
SudoMakeMeAFlag}",contents:{script (...)
```

The flag is therefore CSC{02-SudoMakeMeAFlag}.


#### Challenge 3


The third flag is hidden in the SSL certificate of the https service running on port 443 (that is serving exactly the same content as on port 80). There are two ways to find out whether this service is running.
  1. A port scan will show that the server listens to port 80 and port 443.
  2. A TODO item has been left in css/style.css, asking whether the file works on https.

Opening https://tl0.be/ in a webbrowser will show an alert as the certificate has not been configured correctly. When viewing the certificate details, the following field will be found...
 
```
Organizational Unit (OU): CSC{03-FourFourThreeIsKey}
```

The flag is therefore CSC{03-FourFourThreeIsKey}.


#### Challenge 4

The fourth flag is hidden as a TXT record that belongs to tl0.be.. It can be retrieved using... 
```
$ dig -t txt tl0.be +short
"flag=Q1NDezA0LVlvdXJlQUxpemFyZEhhcnJ5fQ=="
```
Or, without guessing the record type to be “TXT”...
```
$ dig tl0.be ANY
(...)
tl0.be. 3587 IN TXT "flag=Q1NDezA0LVlvdXJlQUxpemFyZEhhcnJ5fQ=="
(...)
```
When base64 decoding this string, you get the flag.
```
$ echo -n "Q1NDezA0LVlvdXJlQUxpemFyZEhhcnJ5fQ==" | base64 -D -
CSC{04-YoureALizardHarry}
```

The flag is therefore CSC{04-YoureALizardHarry}.

#### Challenge 5

The fifth, and final flag, is hidden inside the favicon.ico.

A hint that has already been given that something is phishy about this image is that it resembles a flag. Upon investigation of the file extension (and the file format), the file type can be identified to be an .ico file.

Wikipedia has a detailed description of this file format. It is a container which embeds either BMP or PNG files inside. When investigating this file in a Hex Editor (e.g., HexEd.it), the actual PNG file can be retrieved.

When investigating this PNG file, with an EXIF editor (e.g., Jeffrey Friedl’s Image Metadata Viewer), the following can be found.
```
User Comment: CSC{05-YouAreABoldOne}
```

The flag is therefore CSC{05-YouAreABoldOne}.

### Flag

Note! This challenge consists of five flags!
  * `CSC{01-TastyHeaderForBreakfast}`
  * `CSC{02-SudoMakeMeAFlag}`
  * `CSC{03-FourFourThreeIsKey}`
  * `CSC{04-YoureALizardHarry}`
  * `CSC{05-YouAreABoldOne}`


### Creator
Bjarno Oeyen

