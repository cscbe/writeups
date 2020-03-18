# Tea 2

## Challenge created by Remco Hofman

## Description

> What is this sticky note doing here? What does "NamingIsTheOriginOfAllParticularThings." even mean..?


## Solution

People put passwords on sticky notes all the time, unfortunately.  
But we still haven't found the username.
Again, `grep` helps us out with this one.

`grep account dump_strings.txt`

This gives about 200 results, but right at the end of the list, there are some interesting entries:

```sh
oSELECT * FROM accounts
:SELECT * FROM accounts WHERE email = 'KakuzoOkakura' AND issuer IS NULL
oSELECT * FROM accounts
:SELECT * FROM accounts WHERE email = 'KakuzoOkakura' AND issuer IS NULL
oSELECT * FROM accounts
```

`KakuzoOkakura` seems to be the username!  
The credentials `KakuzoOkakura:NamingIsTheOriginOfAllParticularThings.` work, but then you hit the 2FA page.

The key to solving this one is realizing you have the memory of the user's Google Authenticator.
In order to be able to generate the TOTP token, it needs to have all the basic information in memory.

If you look up how TOTP-based 2FA works you should quickly find out that the key is a Base32 encoded pre-shared secret, but how do we find it?  
The answer is, once again, `grep`:

`grep 'KakuzoOkakura' dump_strings.txt`

Only 26 unique results, 1 of which is quite peculiar:

```sh
'KakuzoOkakuraINJUG62UNBSUG5LQJ5TEQ5LNMFXGS5DZFYXC47IKKakuzoOkakura
```

If you Base32 decode the part delimited by the user's account name, it turns out you've already seen this before:
It's just the first flag!

Now all that's left is to actually derive the right 2FA token and enter it.  
You could either write a simple script for this using a library or use [this website](https://totp.danhersam.com/#/INJUG62UNBSUG5LQJ5TEQ5LNMFXGS5DZFYXC47IK).

After passing the 2FA, you are greeted by the second flag: `CSC{TheBeautifulFoolishnessOfThings}`.
