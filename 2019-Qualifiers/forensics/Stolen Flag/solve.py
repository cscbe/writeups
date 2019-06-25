import pcapy as p
from scapy.all import *
from Crypto.Cipher import ARC4
import re

data = "traffic.pcapng"
packets = rdpcap(data)

pkt_count = 0
key = "VerySecureKey1337\x00"
RC4 = ARC4.new(key)


def parse_decypt(pkt) :
    global pkt_count, RC4
    res = b""
    next_packet = None

    # Packet Type
    offset_0 = struct.unpack("<I", pkt[0:4])[0]

    # If packet header is present
    if offset_0 < 6 :
        
        # Data size
        offset_4 = struct.unpack("<I", pkt[4:8])[0]
    
        # If there is data to fetch
        if offset_4 > 0 :
            # Data
            offset_8 = pkt[8:]
            # If reassembled packet (multiple packets considered as one in the pcap)
            if len(offset_8) > offset_4 :
                # prepare next packet to be decrypted
                next_packet = offset_8[offset_4:]
                # Only decrypt first packet in this call
                offset_8 = offset_8[0:offset_4]
            # Decrypt 
            pkt_count = (pkt_count + 1) & 0xff
            key = b"VerySecureKey1337" + struct.pack("B", pkt_count)
            RC4 = ARC4.new(key)
            res = RC4.encrypt(offset_8)
        # If packet were reassembled, parse second packet
        if next_packet != None :
            parse_decypt(next_packet)
    else :
        # If no packet header, it's a file chunk
        res = RC4.encrypt(pkt)
    # Search for a flag
    res = re.search(b"(CSC{.+})", res)
    if res:
        print("Found a flag : %s " % res.group(0).decode())
        exit()

# Let's iterate through every packet
for packet in packets:
    if packet.haslayer(TCP):
        if len(packet[TCP].payload) > 0 : 
            # Get the TCP data and parse them
            pkt = bytes(packet[TCP].payload)
            parse_decypt(pkt)

            