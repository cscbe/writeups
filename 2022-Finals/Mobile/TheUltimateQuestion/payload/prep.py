import base64, random
data = open("vault-jar2dex.dex", "rb").read()
encoded = base64.b64encode(data)

parts = []
partstemplate = """
<string-array name="parts">
    {}
</string-array>
"""
pp = "<item>{}</item>\n"
pos = 0
length = 2
while True:
    parts.append(encoded[pos:pos+length])
    pos += length
    length += 1

    if pos > len(encoded):
        break

random.shuffle(parts)


ppp = ""
for part in parts:
    ppp += pp.format(part.decode())

print(partstemplate.format(ppp))