# Description

We uncovered this encrypted datacube, can you recover the contents?

N = 634504ee7770f969cfb8d9065fdbe37c58ca33640a0ee82f6d50b0b6a451a18519b83ff730a4fc00232f7244ebd1ec4f1608613fbfcf4838bfec5a53466898eca14a41ece3db9a79b8a7d7460075b45300a011485508210cc534dcb400eaf9c616de3dd0612db41cd0363a5c49269a17ee04be80b50da93a226949b88baceb7d576473e8a2ab0b6dd46073b2f80980e7b45a8b3421fefdfcbdfa8f8262340844a11bf1681b30405967992f5afb3891ad85289eb79ad7e3e71a0861af8eb1b9ebcc3d6d454a193fd78cf7cf496345e50ba516bf86e02f89c21c443a5b8908670860d2ddc6f
c = 14aa1e31e4c5ddcc4da5bf7716da53a532f4bce4ab0cca7489f849981c14edfdc486122c4f74e3d3f0ca375161a8c58b067fdd886e4a3cb29d77a3b2c27580b31ba3b2bba50212df8467655a950257aef8df0591f4a81c82a12216408a5af9a5f988069c5c0b49a7966ea8370dcee275decbc1c081e66ea0c802e0aac8aa33b9ed8eebc55533270c442bbbc81507b40b8a8e36507322ef4ba1371346c0020866791319ac327ae4e87f0af13fbf8e800d4e918d40f6bc7e9534bc60617e3021d40470cb181f1a1da6b755f8cd2291f6249ad0be20024b649b6ba84de31ad4f43823192d048


# Solution
Contestants should guess the value of the public exponent e, which is 3 (the data"cube" is a hint).
The plaintext message is very small, and the encrypted message is only three times as large.
The intention is to bruteforce the decryption by exploiting this fact.

The simplest way to do this is by realizing that in the following identity: m^3 = c + k*N
k will likely be a small integer. Indeed, one can try many small values for k to obtain the flag.
(I consider this to be the canonical solution, and it is the one implemented in the solution
scripts.)
Alternatively, it may also be possible to solve using a variant of Coppersmith's method (but that
is way overkill for this challenge).
