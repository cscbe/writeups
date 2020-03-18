#!/env/bin/python
import socketserver
from base64 import b64decode

VALID_H = "3F34564B0A1FB3AFE3676911FF990B3127BEC0C2"
FLAG = "REDACTED"

MODULUS = 0xE4D114A8D6BDA750718DC4865391DEAF71CDA4624DC92FC720B7C27A1E254F1F73F86888FFB37816ABB2BEDF98DFD35EDB10C40A05C7BE6D881E4C3F1C881E71026B5386E60A76AD5273B446D79901E5557BF1850C726EAEABCF7212F0C6173A61B8C1EF197DA2ACFA3A083FAA7F6246948E263F8F8CEA77562AC990090BB8F80C891ED8732AEE829D4850D8BE54C40F6051FDE7F6A8BA1A0E598EE67582E9FCD998480C23B7B987B830D94B6D054FC98DBD5E77620742524A876FBC7F189987600ABB7BE222C6700AFAE8E6DA3FB442BB772D5ECE4356C552293C2C102A14A2B59434941453E54E1D2F0E677E6E05F2CFA6BDEF8F794DED7F6477CD014C7A8D
EXPONENT = 3

HOST = ''
PORT = 21423

HASH_SIZE = len(VALID_H)
SIGNATURE_SIZE = 256
ASN = b"0!0\t\x06\x05+\x0e\x03\x02\x1a\x05\x00\x04\x14"


def verify_signature(h, signature):
    s = int.from_bytes(signature, 'big')
    m = pow(s, EXPONENT, MODULUS)
    m = m.to_bytes(SIGNATURE_SIZE, byteorder='big')
    if len(m) != SIGNATURE_SIZE:
        return

    if m[0:2] != b"\x00\x01":
        return False

    sep_idx = m.find(b"\x00", 2)
    if sep_idx <= 0:
        return False

    if m[2:sep_idx].count(b"\xff") != sep_idx - 2:
        return False

    asn_start = sep_idx + 1
    if m[asn_start:asn_start+len(ASN)] != ASN:
        return False

    hash_start = asn_start + len(ASN)
    if m[hash_start:hash_start+len(h)] != h:
        return False

    return True


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.send(b"Enter hash: ")
        hex_h = self.request.recv(1024).strip().decode()
        try:
            h = bytes.fromhex(hex_h)
        except Exception as e:
            self.request.send(b"\nIncorrect hash\n")
            return

        self.request.send(b"\nEnter signature: ")
        b64_signature = self.request.recv(4096).strip()
        try:
            signature = b64decode(b64_signature)
        except Exception as e:
            self.request.send(b"\nIncorrect signature\n")
            return

        if hex_h == VALID_H:
            if verify_signature(h, signature):
                self.request.send("Here, get a flag: {}".format(FLAG).encode())
            else:
                self.request.send(b"Incorrect signature")
        else:
            self.request.send(b"Incorrect hash value")


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
