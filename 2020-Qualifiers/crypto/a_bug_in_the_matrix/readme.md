# A bug in the matrix

## Created by David vandorpe

# Description
Hello elite hacker. We've heard you are a fine cryptographer. Can you harvest the flag from the fields of cryptography?

Given:
nc 54.72.64.138 1337
Challenge.hs

# Solution

## GF(2)

This writeup assumes basic familiarity with [GF(2), the Galois Field of two elements](https://en.wikipedia.org/wiki/GF\(2\)). It is equivalent to Z/2Z, which is more commonly known as modulo 2. The important part is that in GF(2), addition corresponds to the logical XOR operation.

## Analyzing the cipher

The cipher is a [Feistel cipher](https://en.wikipedia.org/wiki/Feistel_cipher), with a round function that XOR's with a round key and applies a random round permutation. The round key and permutation are generated separately, but remain unchanged within the same session.

An encryption oracle is given for this cipher.

The key weakness is that XOR'ing with a round key is an affine transformation, and a permutation is a linear transformation (and thus also an affine transformation with a translation of length 0). Because the combination of two (or more) affine transformations is also an affine transformation, the entire cipher can be written as an affine transformation. So there exists a matrix M and vector v such that `cipher = M*plain + v`.

Because both XOR and a permutation are invertible operations, the affine operation is also invertible. This means that the matrix M has a multiplicative inverse (call it M'). 

Formally we can define both the plaintext and ciphertext space as a vector space V over GF(2), with 512 dimensions (the block length). The cipher C is now a transformation `C : V -> V`, that can be written as `C(p) = M*p + v` with M an invertible 512x512 matrix, and v a vector of length 512. 

## Constructing the affine transformation

The vector v as defined above can trivially be obtained by encrypting the zero vector, so `cipher = M*plain+v = M*(0,0,0,0,0,0...0) + v = v`.

Calculating the matrix M is slightly more difficult. If we encrypt a vector that starts with a 1 and the rest are all zeros, then `cipher = M*(1,0,0,0,0,0...0)+v = m0 + v` with m0 being the first column of matrix M. Repeating for each possible basis vector of the plaintext space results in M.

Once both M and v are constructed, the flag can be derived with some simple algebra: `flagEnc = M*flag + v <=> M' * (flagEnc - v) = flag`.


