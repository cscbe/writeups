# Using readlines()
file1 = open('InvisibleInk.txt', 'r')
Lines = file1.readlines()

flag = ""

# Strips the newline character
for line in Lines:
    if len(line.strip()):
        character = line.strip().replace(" ","")
        line = line.replace("\n","").split(character)
        asciival = ord(character)
        before = len(line[0])
        after = len(line[1])
        flag += chr(asciival - before + after)

print(flag)
