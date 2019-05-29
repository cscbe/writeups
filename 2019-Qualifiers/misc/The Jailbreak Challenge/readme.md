## The Jailbreak Challenge

### Description


#### Challenge 1 
> Wake up, NEO. The matrix has you. Follow the White Rabbit. Recover the flag: *link to 5_T1m3s.zip_*


#### Challenge 2

> This is your last chance. After this, there is no turning back. You take the blue pill - the story ends, you wake up in your bed and believe whatever you want to believe. You take the red pill - you stay in Wonderland and I show you how deep the rabbit-hole goes.
> Note: this is the follow-up challenge of The Jail Break Challenge #1


#### Challenge 3

> I know what you're thinking, 'cause right now I'm thinking the same thing. Actually, I've been thinking it ever since I got here: Why oh why didn't I take the BLUE pill?
> Note: this is the follow-up challenge of The Jail Break Challenge #2


### Solution

#### Challenge 1 

We received a zip file named: 5_T1m3s.zip The zip file is encrypted, but the filename gives a hint about the password:
  * 5 characters
  * Using [0-9] and [a-zA-Z]

Can be cracked with john the ripper. Password found: `C99tt`
Once unzipped, we have 4 new files:
  * challenge.pdf
  * flag.txt
  * instructions.asc
  * not_yet.zip

We've got the first flag: CSC{f0b487b82fee5b144808cad2e33f2898}


#### Challenge 2

The pdf file contains an interesting description in his metadata: `Mozart is not a walking dead`

Using PDF extraction tools (like pdf-parser of Didier Stevens), we can extract an embedded hex sequence:

```
$ python pdf-parser.py -o 8 -c challenge.pdf
obj 8 0
Type: /EmbeddedFile 
   Referencing:
   Contains stream
     <<
         /Length 3647
             /Filter /ASCIIHexDecode
                 /Type /EmbeddedFile
>>
'2d2d2d2d2d424547494e205047502050524956415445204b455920424c4f434b2d2d2d2d2d 0a56657273696f6e3a20424350472043232076312e362e312e300a0a6c514f734246785a393 6674243414350594d482b6d6b68526d62776c694b754d64322b3464572b535148454a33452f 71786136655948712f527a7964417877550a6753567a564b61626e76364d4c5572425274763 635536e4c704d33486d6673556562617348715447354d717546446e4773625a796c41477a79 6651675a71694c0a69643174356657787350495754627973456f46734a3645416f68356c625 76d5733726a416762624139684e756a386d413562513474697a5330622b7a6c704d410a5430 555a5232704359386f31377364564e7a7552726f724e6133436955756335554c56775646427 94e39446537454f3373306e486c79735747384b365a4475620a57685563772b6b3876493344 516c5134684d70595169384d6743376a42463234454530344f72463359364b5049615a7a633 3394e4f4f4c684c6669626b7135460a385a465173722b314f4b4b53596d5641474363613044 4a336f6a4e6c6933327966677a44414245424141482f41774d434a4d6447566543347462746 7457672330a58676e563762304874416a7461302b484834445a783456774b56672b69595a46 476c4a394d6c6e70573369376865585548792b4652786c7a7734682b374159750a65515a427 2755a43463132585a392f4f6a62494432706f72544e506b426c6b2b475470676d684b724e2b 724b4c79314779763955744765484544707a465643460a5076334b676d4b3047654f2f58324
3503361564736797163782b533039583735514943387a5a68626b7965614c5a49582b6f4758 486f3656566d396f387258520a5871716f4c4132326e56364f6834496352626a5969634f533 4434a4275454c51786b6c422f39556d324569725965456a705062536e4d4f665a6d72596c6c 656d0a58687562414836635561324f35766274736b3471414c6e6f51446b525943706c556c7 3584879564e7a342b653939636258616c542b626e67506d632b6b6569310a33517142556c4d 3450717a526d3858377a4e5647654d66536e705a6737795350574c384864714939734448447 a634b625832594e35757376383254656775596b0a502f4f456550716f766878505651617244 524a396a5a484e58574253776c63337342307776444149662f45796670377030474b424d763 44c597065426c5941360a735858342f5276506a732f774e3436326a7862774365492f2f6854 525252376456572b3232694b345877526746533977336e736a6b70794c44635368653454370 a727856676f6f58486d42737630324b563350556b715a364469537566686d4a476261687957 4a7256515346626f3343616f7145694d3654476567547751325a430a4e37346561463543354 4796954782b386947306877696f3776534155376a3565624c386e486d712b73755969584544 6647445a7178646a3969333571774367740a30787878665765314644626e694d65437438506 44b66692f5a76734e7733714d314b596d544d486f625836646e665071364953336d62383136 59615a2f4e57610a594c4e6e6e30464a6e3971567166514863756b6d6342425a717550376e6 83963756a6433696a566d34586b4555423438524838354e694741596f654f4a774b570a3035 6250794a5243423032574332765a7557477a7a756e474b6b74492b654e4671583548546e484 66555452b6c4b4854356c5250326d6b6270353061664751680a6d74364d4d714251515a3862 542b714230756e57784c71623161624276786a4c34315a6a5442766d486251685a476c74615 852796153356b61574672623252700a62576c30636d6c7a5147467763484a7659574e6f4c6d 4a6c69514563424241424167414742514a635766656f41416f4a45503132793235502b61413 4472b41480a2f6a526457733477447133374679337073376451695267614b524a5170633834 7a79625474327354746245675342336e2f376b43716d6e31506f7074707239660a4f656d6a7 956454e4f576265645777535248394e36346b7953337536312f7269664a52767a6973472b77 2f3632514e4746497443326f49485a545947444657640a664d79674a7a3932774b3947654f6 6432f39484269456b66332f6873633168445253466a706a36446b504c726972794465685053 7159586279656c56566a74540a597a7838476e3230762b783536724e76347a6578377154344 776482b2f365a4a6a4856694872642f35366948707a566837477176736f4e6867766c7a566c 63410a4a6263625a307a707646796252383755494c6a645149454744476e65717336764d444 86c3165442b31677944546e417334787373376366524834346d566e72560a4272506c6b4c75
4874634366686a3063384536426c30383d0a3d2b6330700a2d2d2d2d2d454e4420504750205 0524956415445204b455920424c4f434b2d2d2d2d2d0a0a>\n'
```

Using an hex to ascii editor (e.g. https://www.rapidtables.com/convert/number/hex-to-ascii.html), we get a PGP private key. In fact, the "description" meta data is the passphrase of the private key. With those information, we can decrypt the containt of instruction.asc (e.g. using https://www.igolder.com/pgp/decryption/) 
The result of the decryption:

```
Second Flag
----------- CSC{47d9a3dffa147610f62e23ca78f5a8f7}
Zip Password
------------
Keep going you are ready for the next stage
```

#### Challenge 3

We can then decrypt the file not_yet.zip. Once decrypted, we get a new zip file: nca408qdnxkf.zip
This time, we have a recursive zip file with random names, we have to write an extraction script that will remove the top level zip after each decryption. If not removed, the recursive decryption will take around 2Tb !!! (takes around 15min to decrypt)

At last decryption, we get 2 files:
  * enterthematrix.zip
  * opensesame.jpg

The zip file is encrypted. To decryption key is viewable in opensesame.jpg --> DECRYPT KEEPER
We can use that password to unzip the last zip. The zip file contains an html file showing an animation from the movie "MATRIX". Looking at the source code, we can notice that the matrix code is a binary sequence. We have to revert and convert the binary to ASCII to get the final flag:

```
$ echo '"1","0","1","1","1","1","1","0","0","0","0","0","1","1","0","0","0","0","1 ","0","0","1","1","0","0","0","1","0","1","1","0","0","0","0","1","0","1"," 1","0","0","1","1","1","0","1","1","0","0","0","1","1","0","0","1","1","0", "0","0","1","0","0","1","1","0","0","0","0","1","1","1","0","0","1","1","0" ,"0","1","1","0","0","0","1","0","0","0","1","1","0","0","0","1","0","1","1 ","0","0","0","1","0","0","0","1","1","0","1","1","0","0","0","1","1","0"," 1","0","0","0","1","1","0","0","0","1","1","0","1","1","0","0","1","1","1", "0","1","1","0","0","1","0","0","1","1","1","0","0","0","0","1","0","1","1" ,"0","0","0","1","0","0","0","1","1","0","1","0","0","1","1","1","0","0","0
","1","1","0","1","1","0","0","0","0","0","1","1","1","0","0","0","1","1"," 0","0","1","1","0","0","0","1","0","0","1","1","0","0","0","1","0","1","1", "0","0","1","1","0","0","1","1","0","0","1","0","0","0","1","1","0","0","0" ,"0","1","0","1","1","0","0","0","1","0","0","0","1","1","0","0","0","0","0 ","1","1","0","0","1","0","1","0","1","1","0","0","0","1","1","0","0","1"," 1","0","1","1","0","1","1","1","1","0","1","1","0","0","0","0","1","0","1", "1","0","0","1","0","1","0","1","1","0","0","0","0","1"' | sed 's/"\(.\)",/\1/g' | sed 's/"//g' | rev | xargs ./bin2ascii.py -b
CSC{f50b4134df869b49761cb4b38df744d0}
```


### Flag
  * `CSC{f0b487b82fee5b144808cad2e33f2898}`
  * `CSC{47d9a3dffa147610f62e23ca78f5a8f7}`
  * `CSC{f50b4134df869b49761cb4b38df744d0}`


### Creator
Dimitri Diakodimitris (https://www.linkedin.com/in/dimitridiakodimitris/)