# A pirate's life for me

## Description

Our new intern designed a new licensing system four our software based on RSA and the hash of the computer it will be run on.
It will allow us to create licenses file for specifics computer and prevent software sharing.

To verify the security of his protocol, we asked him to make a simple python server which is attached and running at the address xxxx and port 21423.

Your goal is to send to the server the signature for the hash `3F34564B0A1FB3AFE3676911FF990B3127BEC0C2`


## Solution
We can see with the provided code that the used algorithm is RSA signature.
The goal is to find a way to create a valid signature for the hash `3F34564B0A1FB3AFE3676911FF990B3127BEC0C2`.

By looking at the verify_signature, we can see that the signature should be

`0001` followed by `FF` then `00` and the hash `3F34564B0A1FB3AFE3676911FF990B3127BEC0C2`.

All of that being as long as the modulus. This scheme is based on PKCS1.5.

All of this is extracted from the signature send through the network by applying the RSA verification.
With the public key having `3` as exponent and `E4D114A8D6BDA750718DC4865391DEAF71CDA4624DC92FC720B7C27A1E254F1F73F86888FFB37816ABB2BEDF98DFD35EDB10C40A05C7BE6D881E4C3F1C881E71026B5386E60A76AD5273B446D79901E5557BF1850C726EAEABCF7212F0C6173A61B8C1EF197DA2ACFA3A083FAA7F6246948E263F8F8CEA77562AC990090BB8F80C891ED8732AEE829D4850D8BE54C40F6051FDE7F6A8BA1A0E598EE67582E9FCD998480C23B7B987B830D94B6D054FC98DBD5E77620742524A876FBC7F189987600ABB7BE222C6700AFAE8E6DA3FB442BB772D5ECE4356C552293C2C102A14A2B59434941453E54E1D2F0E677E6E05F2CFA6BDEF8F794DED7F6477CD014C7A8D` as modulus.

### Forgery
The goal is thus to be able to create a valid signature based on that.
The problem is that we only have access to the public key and not the private.

But there are two things that are not checked:
 * The hash is at the end and there are not other random bits afterwards.
 * The length of the signature is valid.
If we could find a way to have a number such that his cube would be equal to:
    
Our header, `0001FF00` followed by `our hash` and enough `random bytes` to have the correct length.

Here is my python code for it:
```python
from base64 import b64encode

def iroot(x, n): 
    h = 1 
    while h **n < x: 
        h *=2 
    l = h//2 
    while l<h: 
        m = (l+h)//2 
        if l<m and m**n < x: 
            l = m 
        elif h> m and m**n >x: 
            h=m 
        else: 
            return m 
    return m+1 

a = 0x1ff003021300906052b0e03021a050004143f34564b0a1fb3afe3676911ff990b3127bec0c26d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d

r = iroot(a, 3)
b = b64encode(r.to_bytes(85, "big"))
print(b)
```
This will give us a signature for a close enough. If we take the result to the power of 3, we will not recover our a but the change will be in the last bytes which aren't important (they are random).

We can then send this to the server using netcat and get the flag.
