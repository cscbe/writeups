# The Stuffing of Delphi

## Write-up and Challenge by Pieter Hiele

When browsing the API, you will get redirected to the ​/user​ endpoint which returns a single JSON response containing a field “user”, e.g.:

    {"user":"b83ae622d65eb024"}

The description of the challenge also hints that all answers will be provided by the endpoint /flag​. When you go there, it says:

    {"user":false,"error":"The user id should be specified as a GET parameter","flag":false}

Browsing to ​/flag?user=b83ae622d65eb024​ results in: 

    {"user":"delphi","error":"The flag is only available to administrators.","flag":false}

When attempting to tamper with the user identifier, the API will start throwing several errors:

* TypeError:Badinputstring  
* datanotmultipleofblocklength
* Error:Invalidpadding

These errors give the impression that the provided string is actually an encrypted string that is being decrypted. The “invalid padding” error in particular, seems to point in the direction of a Padding Oracle attack, which matches the clues in the title of the challenge.

A padding oracle is a vulnerability that allows an attacker to infer knowledge about a provided encryption string K by executing byte-by-byte operations on the string and sending it to the application. Because the application responds with “invalid padding” if the CBC padding of the decrypted string is incorrect, and another error otherwise, we call the endpoint a padding oracle.

The question becomes: can we abuse the padding oracle to construct our own encrypted string of “admin”? The answer is a resounding yes. There are many online resources that make it easy to automate this, for example by using the Python implementation on https://github.com/mwielgoszewski/python-paddingoracle​ it is possible to find the solution:

We can now feed this to the API: /flag?user=5a49a952c08338503ce1c1c533c8375a ​with success:

    {"user":"té@Ðê​/Jadmin","error":null,"flag":"CSC{communication-is-k ey-even-when-all-you-provide-is-gibberish}"}

Even though we are unable to completely remove the leading random bytes, as a result of the IV (initiation vector) being set by the application, it appears that the API was only checking for the string “admin” in the username. Result!

The flag is ​`CSC{communication-is-key-even-when-all-you-provide-is-gibberish}`​.