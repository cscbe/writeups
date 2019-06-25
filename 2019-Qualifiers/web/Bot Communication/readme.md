## Bot Communication

### Description

> You found a malicious server that looks to serve content via HTTP requests. When you visit the website, you receive an error message. 
> Will you successfully interact with the server?


### Solution

When you visit the webpage, you get a error message “Unknown command: xxx”. 
Check carrefully the command, it looks like Base64. Decode it and you should be able to guess the value… It’s part of the User-Agent.

Bot communication can be performed by Base64 encoding commands as 1st word of the User-Agent (you need a plugin or use curl/wget for this).

The first command that you can try is “HELP” and a list of available commands will be returned. Then, the user can ask for a token via “TOKEN” and a key via “KEY”. 

You should then see some binary content that looks like crypted. Just XOR the TOKEN & KEY to get the flag!

### Flag
`CSC{cadbb3d5182534e09574a7de93509d6f84dc773837f8faef303128554d935ead}`


### Creator
Xavier Mertens

