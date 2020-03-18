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
import sys
sys.stdout.write(b.decode("utf-8"))
