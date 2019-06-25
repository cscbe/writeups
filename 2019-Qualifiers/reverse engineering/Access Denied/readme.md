## Access Denied

### Description

> Our intelligence tells us that E Corp is working on something really dangerous in their Robotics lab. 
> Our inside-man has been trying to get access to the lab for weeks, but the password required to open the door changes daily. 
> 
> Some hours ago, he was able to intercept a binary. He believes that binary is used to update the embedded component that verifies the password. 
> Can you help us recover the lab password before it is changed again? This might be our only shot...


### Solution

The actual challenge is reverse engineering an Arduino binary. To spice things up, the binary is embedded encrypted in an update script. 
Don't worry, the key is in there too :) 


#### Step 1
Decrypt Arduino binary (.elf file). This can be done by isolating the useful lines of the 
update.bin script and removing the rest: 

  `CHECKSUM="67264de22f36c95c203074971ad1da69"`

  `ENCRYPTED="U2FsdGVkX1/v6r0H2hbqdIrHmgsZM89WeCl5m3P9PXs2OUnrro4ejHUIZ+cha8XlV1XA2r33HG3qLzf/KS <SNIP>`

  `DECRYPTED=$(echo $ENCRYPTED | openssl enc -aes-128-cbc -a -d -salt -pass pass:$CHECKSUM -A)`

  `echo $DECRYPTED | base64 -D > input.elf`


#### Step 2
Check that the elf file is decrypted OK :P 

  ```
  \> file input.elf
  input.elf: ELF 32-bit LSB executable, Atmel AVR 8-bit, version 1 (SYSV), statically linked, with debug_info, not stripped
  ```


#### Step 3
Dissassemble binary. Online dissasembler does a pretty good job with AVR binaries: 

https://onlinedisassembler.com/odaweb

Alternative: use `avr-objdump -D input.elf`. avr-objdump is part of the avr-binutils package.
(brew install avr-binutils). 


#### Step 4
Starting at address 0x1bc you'll see labels checkByte0 - checkByte14. 
The password is checked by XORing it byte by byte with a key, and checking the result against 
the ciphertext. To get the plaintext password, we just have to XOR the key with the ciphertext :) 

Example: for the first label, checkByte0, the code works likewise: 

```
ldi r17, 0x4F ; 79             -> load integer 79 into register r17 
lds r18, 0x0230          -> load first byte of user input from memory into r18
eor r17, r18           -> XOR r17 and r18, store result into r17
cpi r17, 0x0C ; 12       -> compare r17 with integer 12 
brne  .+2       ;  0x000001ca <checkByte1> -> if not OK, jump to next comparison 
inc r16              -> if OK, increment the number of OK bytes 
```

So just do 79 ^ 12, which results in `C`. 

Keep XORing until the flag is revealed.

### Flag
`CSC{aVr_<3_AsM} `


### Creator
Théo Rigas

