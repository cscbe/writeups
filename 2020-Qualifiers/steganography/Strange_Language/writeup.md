# Challenge
This is a challenge about all different types of encoding, it starts with a flag and is then encoded in different formats. The challenge can leave out several steps in order to decrease the difficulty.

## Step 1
`csc{iusedtoruletheworld-fallenkingdom}`

## Step 2
[Minecraft enchantment table translator](https://lingojam.com/StandardGalacticAlphabet):
`ᓵᓭᓵ{╎⚍ᓭᒷ↸ℸ ̣ 𝙹∷⚍ꖎᒷℸ ̣ ⍑ᒷ∴𝙹∷ꖎ↸-⎓ᔑꖎꖎᒷリꖌ╎リ⊣↸𝙹ᒲ}`

## Step 3
base64 to keep the charset, but with a twist: it's [UTF-7](https://www.base64encode.org/)
`K0ZQVVU3UlQxQUhzbFRpYU5GTzBVdHlHNElUZyArQXlNICsyRFhlZVNJM0pvMmxqaFMzSVRnICtBeU0gK0kxRVV0eUkwMkRYZWVTSTNwWTRodUEtLStJNU1WRWFXT3BZNFV0ekRxcFl3bFRqRHFJcU1odU5nMTNua1VzZ0I5LQ==`

## Step 4
[base58 encode](https://www.browserling.com/tools/base58-encode)
`C3RPJaCzLt4twbYv2LNUT3c6zdP531JtwCH6m4vpmc9jGHXvEEy3GswXonR7TkC41ZF17fXcYd8Mt36BpgKWw7vbWuy3pqcAdCHqgVp3NkP92ve6t3W3KoFUiqFfW7HMXGCZfAUjGRJPR5hx9JzdFzWcLNjVkNtZ8wPbqkZr9cBVrWcpCvkfuJDMh4JA9pu1iVkEkgk3yJ51wfANxcPmhU6Zq2z6GzLEBanwdfv5u24`

## Step 5
To base85 (cyberchef)
```
6ShV:8mt)59QW+5G@F]u1/(GC<&8#BH=Ti01GMLDG=+nZD)?ETD.>S@7n?a*77DJX7rrlVDf/H3<,4iX0j7%$2eH0%=_'KdF>GgAE+_gFG;j\S=*8dEE,fARA4&n-B3&t-:2<Zd13R4eF>HuS95d:"BlQUS=#WZE=@Y_^AjKF37oDrU;Di-43D+U.7XA-G9MT>'CJJtT3-S2.EGJ`u3FbBVE`Zai6[!6WF\5%rBJ`=I3H0*qBi]"<CM.E=GtKqKG@j-9G[jQeBN6roEADhu7s[it6=FbUA7g!BFYYc
```

## Step 6
To hex
`36 53 68 56 3a 38 6d 74 29 35 39 51 57 2b 35 47 40 46 5d 75 31 2f 28 47 43 3c 26 38 23 42 48 3d 54 69 30 31 47 4d 4c 44 47 3d 2b 6e 5a 44 29 3f 45 54 44 2e 3e 53 40 37 6e 3f 61 2a 37 37 44 4a 58 37 72 72 6c 56 44 66 2f 48 33 3c 2c 34 69 58 30 6a 37 25 24 32 65 48 30 25 3d 5f 27 4b 64 46 3e 47 67 41 45 2b 5f 67 46 47 3b 6a 5c 53 3d 2a 38 64 45 45 2c 66 41 52 41 34 26 6e 2d 42 33 26 74 2d 3a 32 3c 5a 64 31 33 52 34 65 46 3e 48 75 53 39 35 64 3a 22 42 6c 51 55 53 3d 23 57 5a 45 3d 40 59 5f 5e 41 6a 4b 46 33 37 6f 44 72 55 3b 44 69 2d 34 33 44 2b 55 2e 37 58 41 2d 47 39 4d 54 3e 27 43 4a 4a 74 54 33 2d 53 32 2e 45 47 4a 60 75 33 46 62 42 56 45 60 5a 61 69 36 5b 21 36 57 46 5c 35 25 72 42 4a 60 3d 49 33 48 30 2a 71 42 69 5d 22 3c 43 4d 2e 45 3d 47 74 4b 71 4b 47 40 6a 2d 39 47 5b 6a 51 65 42 4e 36 72 6f 45 41 44 68 75 37 73 5b 69 74 36 3d 46 62 55 41 37 67 21 42 46 59 59 63`

## Step 7
Convert the hex to a weird file
e.g. mumbo.bin

## CyberChef
### To Challenge
step 1 and step 2 are done manually
https://gchq.github.io/CyberChef/#recipe=Encode_text('UTF-7%20(65000)'/disabled)To_Base64('A-Za-z0-9%2B/%3D'/disabled)To_Base58('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')To_Base85('!-u',false)To_Hex('Space',0)&input=SzBaUVZWVTNVbFF4UVVoemJGUnBZVTVHVHpCVmRIbEhORWxVWnlBclFYbE5JQ3N5UkZobFpWTkpNMHB2TW14cWFGTXpTVlJuSUN0QmVVMGdLMGt4UlZWMGVVa3dNa1JZWldWVFNUTndXVFJvZFVFdExTdEpOVTFXUldGWFQzQlpORlYwZWtSeGNGbDNiRlJxUkhGSmNVMW9kVTVuTVROdWExVnpaMEk1TFE9PQ

### Solution using CyberChef

https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')From_Base85('!-u')From_Base58('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz',true)From_Base64('A-Za-z0-9%2B/%3D',true)Decode_text('UTF-7%20(65000)')&input=MzYgNTMgNjggNTYgM2EgMzggNmQgNzQgMjkgMzUgMzkgNTEgNTcgMmIgMzUgNDcgNDAgNDYgNWQgNzUgMzEgMmYgMjggNDcgNDMgM2MgMjYgMzggMjMgNDIgNDggM2QgNTQgNjkgMzAgMzEgNDcgNGQgNGMgNDQgNDcgM2QgMmIgNmUgNWEgNDQgMjkgM2YgNDUgNTQgNDQgMmUgM2UgNTMgNDAgMzcgNmUgM2YgNjEgMmEgMzcgMzcgNDQgNGEgNTggMzcgNzIgNzIgNmMgNTYgNDQgNjYgMmYgNDggMzMgM2MgMmMgMzQgNjkgNTggMzAgNmEgMzcgMjUgMjQgMzIgNjUgNDggMzAgMjUgM2QgNWYgMjcgNGIgNjQgNDYgM2UgNDcgNjcgNDEgNDUgMmIgNWYgNjcgNDYgNDcgM2IgNmEgNWMgNTMgM2QgMmEgMzggNjQgNDUgNDUgMmMgNjYgNDEgNTIgNDEgMzQgMjYgNmUgMmQgNDIgMzMgMjYgNzQgMmQgM2EgMzIgM2MgNWEgNjQgMzEgMzMgNTIgMzQgNjUgNDYgM2UgNDggNzUgNTMgMzkgMzUgNjQgM2EgMjIgNDIgNmMgNTEgNTUgNTMgM2QgMjMgNTcgNWEgNDUgM2QgNDAgNTkgNWYgNWUgNDEgNmEgNGIgNDYgMzMgMzcgNmYgNDQgNzIgNTUgM2IgNDQgNjkgMmQgMzQgMzMgNDQgMmIgNTUgMmUgMzcgNTggNDEgMmQgNDcgMzkgNGQgNTQgM2UgMjcgNDMgNGEgNGEgNzQgNTQgMzMgMmQgNTMgMzIgMmUgNDUgNDcgNGEgNjAgNzUgMzMgNDYgNjIgNDIgNTYgNDUgNjAgNWEgNjEgNjkgMzYgNWIgMjEgMzYgNTcgNDYgNWMgMzUgMjUgNzIgNDIgNGEgNjAgM2QgNDkgMzMgNDggMzAgMmEgNzEgNDIgNjkgNWQgMjIgM2MgNDMgNGQgMmUgNDUgM2QgNDcgNzQgNGIgNzEgNGIgNDcgNDAgNmEgMmQgMzkgNDcgNWIgNmEgNTEgNjUgNDIgNGUgMzYgNzIgNmYgNDUgNDEgNDQgNjggNzUgMzcgNzMgNWIgNjkgNzQgMzYgM2QgNDYgNjIgNTUgNDEgMzcgNjcgMjEgNDIgNDYgNTkgNTkgNjM
