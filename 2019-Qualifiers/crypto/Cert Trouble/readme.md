## Cert Trouble

### Description

> One of our servers has been compromised by the famous Russian hacker group Fancybear last year. After analysis, we have found that no information has been leaked but latest CIA espionage report is contradictory: they have in their possession sensitive information from our compromised server.<br />We have tracked every single outbound bytes from day one on this server, we didn't find anything leaked. We still have one doubt: a clear signed XML file that was send regularly somewhere in Russian routed from another compromised private desktop in Belgium. We have sent this signed cleartext sample to our best analysts but they didn't find anything leaked. We are sure that some information is leaked from the sample but we have no idea how they do it. 
> Can you please tell us how the Russian leaked information through this sample

### Solution

Follow the following steps to extract the flag out of the signature:

  1. Paste X509 certificate in certificate.crt and add `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----`
  2. Paste Signature in 'signature.sig'
  3. `cat signature.sig | base64 -D > signature.sig.bin`
  4. `openssl x509 -in certificate.crt -pubkey -noout > pubkey.pem`
  5. `openssl rsautl -verify -in signature.sig.bin -inkey pubkey.pem -pubin -raw`

### Flag
`CSC{s3cr3t_s1gn4tur3s_f0r_th3_w1n}`


### Creator
Olivier Buez

