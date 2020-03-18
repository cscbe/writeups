#! /usr/bin/env python3
"""
Verify whether the challenge "The pie is not a lie" is working properly.
"""
import subprocess
from pathlib import Path
import zipfile
import os
import binascii
import shutil
import sys

if os.name != 'nt':
    print("This needs to run on Windows")
    sys.exit(1)

temp_dir = "challenge_checker_temp"
expected_dir = Path.home() / ".user"
p1 = Path('open_the_gate_now')
p2 = Path('JBQWG23FOIQGC3DFOJ2A====')

try:
    os.mkdir(temp_dir)
    with zipfile.ZipFile("artifact.zip", 'r') as f:
        f.extractall(temp_dir)
    
    with open(os.path.join(temp_dir, "artifact.hex"), 'r') as f:
        with open(os.path.join(temp_dir, "binary.exe"), 'wb') as f2:
            f2.write(binascii.unhexlify(f.read().strip()))
    
    p1.touch()
    p2.write_text("Please run!")

    subprocess.check_output([os.path.join(temp_dir, "binary.exe"), "4242"])
    
    p = expected_dir / "pie.png"
    if not p.exists():
        print("Challenge broken: image path not found")
    else:
        print("Challenge looks ok: verify whether the flag is visible on the bottom of the image at {}. You can delete it afterwards.".format(p))
except Exception as e:
    print("Challenge broken: {}".format(repr(e)))
finally:
    if p1.exists():
        os.remove(str(p1))
    if p2.exists():
        os.remove(str(p2))
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
        

