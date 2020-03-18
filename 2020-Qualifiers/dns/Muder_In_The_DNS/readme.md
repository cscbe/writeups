# Initiation
* The participants get a PCAP named cluedo.pcap, with the hint "A PCAP isn't a murder mystery game"
* Extra hints that can be given
    * Who killed (Dr.) Black?
    * What's in a NAME?
    * WHOIS it we're looking for?
    * In the living room, with a candle stick...
    
# Solution
1. Read through the pcap
    * There is a http connection serving a confession to the domain www.i-killed-black.be
    ```
    <html>
        <head>
            <title>Confessions of a murderer.</title>
        </head>
        <body>
            <h1>I killed him...</h1>
            <p>
                When I arrived home today, I found Mr Black in our house.
                I was furious, he should not have been there!
                Blinded by anger I picked the nearest object I could find...
                I don't remember exactly what happened next, but I killed Mr Black.
            </p>
        </body>
    </html>
    ``` 
    from www.i-killed-black.be, with corresponding ns-lookups

2. The SOA record reveils a "hidden" master server inthelivingroom.i-killed-black.be
    * The hidden master allows full zone transfer, but all clues can be found without actually transfering the zone.
3. The zone contains a top-level TXT-record
    * this refers to who   
     who.i-killed-black.be is a CNAME of murderer.i-killed-black.be 
    * it also tips to how.i-killed-black.be 
4. The txt-record for murderer.i-killed-black.be hints you to search further on "who i am" whoami.i-killed-black.be is a CNAME for whois.i-killed-black.be
5. whois i-killed-black.be is a whois-server and listens on port 43 (=default whois port)
    * Ask `whois -h whois.i-killed-black.be murderer.i-killed-black.be`  
    This gives you a response that hints that you need know about the weapon.
6. How i-killed-black.be has a TXT record that refers to with-a-candle-stick.i-killed-black.be 
    * Ask `whois -h whois.i-killed-black.be with-a-candlestick.i-killed-black.be` and you will get the flag. 

      `CSC{It was Colonel Mustard, in the living room, with a candle stick}`


You can discover most of this from dns-queries, but it becomes a lot easier if you figure out that AXFR is allowed so you can read the zonefile.



