# The pie is not a lie

## Description
This artifact was found on some Windows machines by coincidence. There was no time to investigate, but I extracted the artifact and saved it as a hex dump. Maybe you can have a look?

## Tools used
- python-exe-unpacker: https://github.com/countercept/python-exe-unpacker
- uncompyle6: https://pypi.org/project/uncompyle6/

## Solution

### Step 1
First extract the artifact from the zip file and convert the hexdump back to binary format.

On linux this can be done with the following command:
``` 
xxd -p -r artifact.hex > binary.exe
```

### Step 2
Now that we have the executable, we can try to run it and see what it does (Do this in a VM, as you do not want to run random stuff on your main computer system). 

Running it just seems to print the following:
```This is it:
3.14159265358979323846
The cake might be a lie, but the pie is not.
```

More information needs to be found by looking at the executable itself.
For example running the strings command provides enough information to conclude that the executable contains python code and some other files.


### Step 3
Now that we know that python code was packed into this executable, we can try to identify which packer was used (pyinstaller, py2exe, ...).
Or to make our lives easier we can just run python-exe-unpacker which automatically detects which one was used and then proceeds with the unpacking.

```
python3 python-exe-unpacker/python_exe_unpack.py -i binary.exe
```

This command gives the following output:

```
[*] On Python 3.8
[*] Processing binary.exe
[*] Pyinstaller version: 2.1+
[*] This exe is packed using pyinstaller
[*] Unpacking the binary now
[*] Python version: 38
[*] Length of package: 21047543 bytes
[*] Found 956 files in CArchive
[*] Beginning extraction...please standby
[*] Found 258 files in PYZ archive
[*] Successfully extracted pyinstaller exe.
```

The script detected that the executable contains python 3.8 code and was packed using pyinstaller. More importantly, it also sucessfully extracted quite some files from the executable.

In case python-exe-unpack is not run with the same python version as the one used to create the code it will output a warning telling you to run it with python 3.8.


### Step 4
The script extracted the files to the directory unpacked/binary.exe/.
When going through the list of files, three of them look especially interesting:
- main
- drop.exe
- img.jpg

So it looks like the executable contains another executable with the suspicious name drop.exe. There is also an image called img.jpg that looks interesting or maybe it's just an image.

![img.jpg](./write-up_images/img.jpg)

We try to run drop.exe to figure out what it does (again, use a VM and do not run random code on your main computer system) and just get the following output:

```
Tampering protection detected suspicious activity
```

### Step 5
As we do not know what drop.exe exactly does, we first check what the main file contains as this is the code that is actually executed when running the executable binary.exe.

As the python code is compiled, we cannot read all of the code, but using the strings command again already provides some information of what the code might be doing:

```
$ strings main 
rfe	
msgr
main.py
printer
RandomExceptionN
__name__
__module__
__qualname__r
RandomException2Nr
Something went wrong)
handle_error1
.tempz
drop.exez
img.jpg)
_MEIPASS
	Exception
path
abspath
subprocess
shutil
exists
rmtree
join
getcwd
mkdir
copyfile
check_output)
handle_error2
print)
limit
decimal
counter
calc$
Are you sure? (y/n): 
Ok then, you asked for this ...r1
That's what I thought...i
You have reached the gates...
open_the_gate_nowz!but it seems you are not worthy.
This is it: r'
z,The cake might be a lie, but the pie is not.z
Nice one, you broke it...)
lenr
argv
inputr+
ValueError
openr
main?
__main__)
<module>
```

We see a reference to the other files that already looked interesting (drop.exe and img.jpg) and who is familiar with python will also notice strings (the subprocess module and the method check_output) that could indicate that this code might be trying to run the other executable. We also recogize some of the strings that were printed when running the executable.


### Step 6
As we would like to confirm what the code is actually doing, we need to decompile the main file. 

To accomplish this we can use uncompyle6. We first add the pyc extension to the filename and then run the command.

```
uncompyle6 main.pyc
```

This seems to throw an error:

```
File "/usr/local/lib/python3.8/site-packages/xdis/load.py", line 143, in load_module_from_file_object
    float_version = float(magics.versions[magic][:3])
KeyError: b'\xe3\x00\x00\x00'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/bin/uncompyle6", line 10, in <module>
    sys.exit(main_bin())
  File "/usr/local/lib/python3.8/site-packages/uncompyle6/bin/uncompile.py", line 193, in main_bin
    result = main(src_base, out_base, pyc_paths, source_paths, outfile,
  File "/usr/local/lib/python3.8/site-packages/uncompyle6/main.py", line 319, in main
    deparsed = decompile_file(
  File "/usr/local/lib/python3.8/site-packages/uncompyle6/main.py", line 186, in decompile_file
    (version, timestamp, magic_int, co, is_pypy, source_size) = load_module(
  File "/usr/local/lib/python3.8/site-packages/xdis/load.py", line 111, in load_module
    return load_module_from_file_object(
  File "/usr/local/lib/python3.8/site-packages/xdis/load.py", line 150, in load_module_from_file_object
    raise ImportError(
ImportError: Unknown magic number 227 in main.pyc
```

It does not recognize the magic bytes of the pyc file which probably means that the magic header is wrong or missing (some googling here can save the day).
We need to get the correct python 3.8 pyc file header and add it in front of the file. We can for example find this header by looking at other pyc files compiled by python 3.8.

The following hexstring was found to be a correct header: 550d0d0a00000000e32d3f5e4b000000

We can add it to the file with the following command:

```
printf "\x55\x0d\x0d\x0a\x00\x00\x00\x00\xe3\x2d\x3f\x5e\x4b\x00\x00\x00" | cat - main > main.pyc
```

Running uncompyle6 again now gives output:

```
# uncompyle6 version 3.6.3
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.0 (default, Feb  8 2020, 16:21:25) 
# [GCC 8.3.0]
# Embedded file name: main.py
# Size of source mod 2**32: 75 bytes

<decompiled code left out for brevity>

```

# Step 7
We can finally have a look at the actual code and locate some interesting functionality in the function handle_error2.
It indeed copies the hidden executable to a path under the current directory and executes it afterwards.

```
def handle_error2():
    try:
        bp = sys._MEIPASS
    except Exception:
        bp = os.path.abspath('.')
    else:
        import subprocess, shutil
        try:
            try:
                tpd = os.path.join(os.getcwd(), '.temp')
                os.mkdir(tpd)
                p = os.path.join(bp, 'drop.exe')
                tp = os.path.join(tpd, 'drop.exe')
                shutil.copyfile(p, tp)
                subprocess.check_output([tp, os.path.join(bp, 'img.jpg')])
            except Exception as e:
                try:
                    pass
                finally:
                    e = None
                    del e

        finally:
            if os.path.exists(tpd):
                shutil.rmtree(tpd)
```

We can see that this "error handling" method is triggered in the main method when RandomException2 is raised. 

This exception is only raised under two specific conditions: the value of l, passed as an argument, needs to be equal to 4242 and the file "open_the_gate_now" needs to exist in the same directory. However, those two conditions do not matter anymore as we already know that the executable drop.exe is run with the image img.jpg as an argument.

```
def main():
    try:
        try:
            if len(sys.argv) == 1:
                l = 20
            else:
                l = int(sys.argv[1])
                if l >= 10000:
                    r = input('Are you sure? (y/n): ')
                    if r == 'y':
                        print('Ok then, you asked for this ...')
                    else:
                        if r == 'n':
                            print("That's what I thought...")
                            raise RandomException()
                        else:
                            raise ValueError()
                else:
                    if l == 4242:
                        print('You have reached the gates...')
                        try:
                            with open('open_the_gate_now'):
                                pass
                        except Exception:
                            print('but it seems you are not worthy.\n')
                        else:
                            raise RandomException2()
                ds = calc(l)
                i = 0
                print('This is it: ')
                for d in ds:
                    i += 1
                    print(d, end='')
                    if i == 50:
                        print('')
                        i = 0

        except RandomException:
            handle_error1()
        except RandomException2:
            handle_error2()
        else:
            print('The cake might be a lie, but the pie is not.')
    except Exception as e:
        try:
            print('Nice one, you broke it...')
        finally:
            e = None
            del e
```


### Step 8
We run the executable drop.exe with the name of the jpg file as an argument, just like the binary does.

```
drop.exe img.jpg
```

Unfortunatly, this just give the same output:

```
Tampering protection detected suspicious activity
```

Time to go deeper and investigate the drop.exe executable.


### Step 9
By doing the same for drop.exe as we did for the original executable, we find out this is again an executable containing python code. Luckily we already know how to tackle this.

We again run python-exe-unpacker:

```
$ python3 python-exe-unpacker/python_exe_unpack.py -i drop.exe
[*] On Python 3.8
[*] Processing drop.exe
[*] Pyinstaller version: 2.1+
[*] This exe is packed using pyinstaller
[*] Unpacking the binary now
[*] Python version: 38
[*] Length of package: 12207430 bytes
[*] Found 972 files in CArchive
[*] Beginning extraction...please standby
[*] Found 510 files in PYZ archive
[*] Successfully extracted pyinstaller exe.
```

Files are unpacked now to unpacked/drop.exe/ and we locate the main file, which is called drop in this case.
We follow the same procedure as in step 5 to decompile it and get the result.


### Step 10
We investigate the main method of the decompiled code and see that the code opens the image and seems to write the output of the use_the_magic method on top of the image before writing it to the path .user/pie.png in the home directory of the user.

This does not seem to happen at the moment since we get the message printed in the exception handler block.

```
def main():
    global initializer
    from PIL import Image, ImageDraw, ImageFont
    from pathlib import Path
    try:
        arg = sys.argv[1]
        t = os.path.joinstr(Path.home)'.user'
        if not os.path.exists(t):
            os.mkdir(t)
        f = os.path.joint'pie.png'
        fnt = ImageFont.truetype'arial.ttf'25
        image = Image.open(arg)
        draw = ImageDraw.Draw(image)
        initializer = arg
        m = use_the_magic()
        draw.text((390, 1000), ('This is what you came for: {}'.format(m)), font=fnt, fill=(255, 255, 0))
        image.save(f)
    except Exception as e:
        try:
            print('Tampering protection detected suspicious activity')
        finally:
            e = None
            del e
```


### Step 11
To find out what goes wrong, we look further into other parts of the code. The use_the_magic method looks interesting as this is supposed to return "what we came for" (Spoiler: it's indeed the flag).

Unfortunatly, the readability of the decompiled code in this method is not as good as the rest of the code due to a parse error:

```
def use_the_magic--- This code section failed: ---

  14         0  LOAD_CONST               0
             2  LOAD_CONST               None
             4  IMPORT_NAME              platform
             6  STORE_FAST               'platform'

  15         8  LOAD_STR                 'ilak'
            10  LOAD_CONST               None
            12  LOAD_CONST               None
            14  LOAD_CONST               -1
            16  BUILD_SLICE_3         3 
            18  BINARY_SUBSCR    
            20  LOAD_FAST                'platform'
            22  LOAD_METHOD              platform
            24  CALL_METHOD_0         0  ''
            26  LOAD_METHOD              lower
            28  CALL_METHOD_0         0  ''
            30  COMPARE_OP               in
            32  POP_JUMP_IF_FALSE    64  'to 64'

  16        34  LOAD_GLOBAL              print
            36  LOAD_GLOBAL              base64
            38  LOAD_METHOD              b32decode
            40  LOAD_GLOBAL              ha
            42  CALL_METHOD_1         1  ''
            44  LOAD_METHOD              decode
            46  LOAD_GLOBAL              utf_32_be
            48  CALL_METHOD_1         1  ''
            50  CALL_FUNCTION_1       1  ''
            52  POP_TOP          

  17        54  LOAD_GLOBAL              sys
            56  LOAD_METHOD              exit
            58  LOAD_CONST               1
            60  CALL_METHOD_1         1  ''
            62  POP_TOP          
          64_0  COME_FROM            32  '32'

  18        64  LOAD_GLOBAL              os
            66  LOAD_METHOD              stat
            68  LOAD_GLOBAL              initializer
            70  CALL_METHOD_1         1  ''
            72  LOAD_ATTR                st_size
            74  STORE_DEREF              's'

  19        76  LOAD_CLOSURE             's'
            78  BUILD_TUPLE_1         1 
            80  LOAD_LISTCOMP            '<code_object <listcomp>>'
            82  LOAD_STR                 'use_the_magic.<locals>.<listcomp>'
            84  MAKE_FUNCTION_8          'closure'
            86  LOAD_GLOBAL              range
            88  LOAD_CONST               2
            90  LOAD_CONST               10
            92  CALL_FUNCTION_2       2  ''
            94  GET_ITER         
            96  CALL_FUNCTION_1       1  ''
            98  STORE_FAST               'magic'

  20       100  BUILD_LIST_0          0 
           102  STORE_FAST               'k'

  21       104  LOAD_GLOBAL              open
           106  LOAD_GLOBAL              initializer
           108  LOAD_STR                 'rb'
           110  CALL_FUNCTION_2       2  ''
           112  SETUP_WITH          174  'to 174'
           114  STORE_FAST               'f'

  22       116  LOAD_CONST               True
           118  STORE_FAST               'b'

  23       120  LOAD_CONST               0
           122  STORE_FAST               'j'

  24       124  LOAD_FAST                'b'
           126  POP_JUMP_IF_FALSE   170  'to 170'

  25       128  LOAD_FAST                'f'
           130  LOAD_METHOD              read
           132  LOAD_CONST               1
           134  CALL_METHOD_1         1  ''
           136  STORE_FAST               'b'

  26       138  LOAD_FAST                'j'
           140  LOAD_CONST               1
           142  BINARY_ADD       
           144  LOAD_FAST                'magic'
           146  COMPARE_OP               in
           148  POP_JUMP_IF_FALSE   160  'to 160'

  27       150  LOAD_FAST                'k'
           152  LOAD_METHOD              append
           154  LOAD_FAST                'b'
           156  CALL_METHOD_1         1  ''
           158  POP_TOP          
         160_0  COME_FROM           148  '148'

  28       160  LOAD_FAST                'j'
           162  LOAD_CONST               1
           164  INPLACE_ADD      
           166  STORE_FAST               'j'
           168  JUMP_BACK           124  'to 124'
         170_0  COME_FROM           126  '126'
           170  POP_BLOCK        
           172  BEGIN_FINALLY    
         174_0  COME_FROM_WITH      112  '112'
           174  WITH_CLEANUP_START
           176  WITH_CLEANUP_FINISH
           178  END_FINALLY      

  29       180  LOAD_CONST               0
           182  LOAD_CONST               None
           184  IMPORT_NAME              codecs
           186  STORE_FAST               'codecs'

  30       188  LOAD_FAST                'codecs'
           190  LOAD_METHOD              encode
           192  LOAD_CONST               b''
           194  LOAD_METHOD              join
           196  LOAD_FAST                'k'
           198  CALL_METHOD_1         1  ''
           200  LOAD_METHOD              hex
           202  CALL_METHOD_0         0  ''
           204  LOAD_GLOBAL              str
           206  LOAD_CONST               31
           208  CALL_FUNCTION_1       1  ''
           210  LOAD_STR                 'tor'
           212  BINARY_ADD       
           214  LOAD_CONST               None
           216  LOAD_CONST               None
           218  LOAD_CONST               -1
           220  BUILD_SLICE_3         3 
           222  BINARY_SUBSCR    
           224  CALL_METHOD_2         2  ''
           226  LOAD_METHOD              encode
           228  LOAD_GLOBAL              utf_32_be
           230  CALL_METHOD_1         1  ''
           232  STORE_FAST               'key'

  31       234  LOAD_GLOBAL              base64
           236  LOAD_METHOD              b85decode
           238  LOAD_STR                 'bZBXFX>)FGbaZHCW^7?+'
           240  CALL_METHOD_1         1  ''
           242  STORE_FAST               'iv'

  32       244  LOAD_GLOBAL              Cipher
           246  LOAD_GLOBAL              algorithms
           248  LOAD_METHOD              AES
           250  LOAD_FAST                'key'
           252  CALL_METHOD_1         1  ''
           254  LOAD_GLOBAL              modes
           256  LOAD_METHOD              CBC
           258  LOAD_FAST                'iv'
           260  CALL_METHOD_1         1  ''
           262  LOAD_GLOBAL              default_backend
           264  CALL_FUNCTION_0       0  ''
           266  LOAD_CONST               ('backend',)
           268  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
           270  STORE_FAST               'cipher'

  33       272  LOAD_FAST                'cipher'
           274  LOAD_METHOD              decryptor
           276  CALL_METHOD_0         0  ''
           278  STORE_FAST               'decryptor'

  34       280  LOAD_GLOBAL              open
           282  LOAD_GLOBAL              ha
           284  CALL_FUNCTION_1       1  ''
           286  SETUP_WITH          318  'to 318'
           288  STORE_FAST               'f'

  35       290  LOAD_FAST                'f'
           292  LOAD_METHOD              readline
           294  CALL_METHOD_0         0  ''
           296  LOAD_STR                 'Please run!'
           298  COMPARE_OP               !=
       300_302  POP_JUMP_IF_FALSE   314  'to 314'

  36       304  LOAD_GLOBAL              sys
           306  LOAD_METHOD              exit
           308  LOAD_CONST               1
           310  CALL_METHOD_1         1  ''
           312  POP_TOP          
         314_0  COME_FROM           300  '300'
           314  POP_BLOCK        
           316  BEGIN_FINALLY    
         318_0  COME_FROM_WITH      286  '286'
           318  WITH_CLEANUP_START
           320  WITH_CLEANUP_FINISH
           322  END_FINALLY      

  37       324  LOAD_FAST                'decryptor'
           326  LOAD_METHOD              update
           328  LOAD_GLOBAL              encrypted
           330  CALL_METHOD_1         1  ''
           332  LOAD_FAST                'decryptor'
           334  LOAD_METHOD              finalize
           336  CALL_METHOD_0         0  ''
           338  BINARY_ADD       
           340  LOAD_METHOD              decode
           342  LOAD_GLOBAL              utf_32_be
           344  CALL_METHOD_1         1  ''
           346  RETURN_VALUE     
            -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 172
```

However, we can still find out what it is doing. It looks to be opening the initializer file (which is set to the image passed as argument to the main method). Based on this file it tries to AES decrypt the value defined as encrypted at the top of the file.

```
encrypted = b'\xf6u\x8f]\xbf\x90\x1e\xed5x\xa2\xc0\xa6t\xc9\x9a\xbf-`kJ0\xa1q[\xf0C\xf4\x80.\xddY\x82s\x83[\x01A\x9c6;\xaf\x17\x194\xd3h\x8a\xa1\xe9\x9dT\xb5\xe9+?W\x8aZA\xb5\xd3\x06\x8b'
```

The decryption process requires an initialization vector and a key. The iv is already defined base85 encoded in the code and the key seems to be computed based on specific bytes from the loaded image file. Which specific bytes exactly is calculated by calling the use_the_magic method for the numbers 2 to 9. The resulting bytes are concatenated and converted to a hex string, which is then encoded ROT13 to get the actual key being used. What it is exactly doing to get the bytes is not that important if we can get the executable to run the code for us. Spoiler: the get_magic method is calculating the nth numer in the look and say number sequence (https://en.wikipedia.org/wiki/Look-and-say_sequence).

More at the end of the use_the_magic method, just before finalizing the decryption process, it seems to try and open the file with the name stored in variable ha. This one is defined as "JBQWG23FOIQGC3DFOJ2A====". This file obviously does not exist, so we create it in the same directory as drop.exe. The code also checks whether the file contains the line "Please run!" or it will terminate.


### Step 12
After creating the file containing "Please run!" in the same directory we run the executable again:

```
drop.exe img.jpg
```

This time we get no output so we assume everything is ok now and check if HOME_DIR/.user/, the path mentioned in step 9 when analyzing the main method, exists.

We find out that it was created now and that it contains the file pie.png. The image is the same as the one passed to the binary, but now also containing the flag written at the bottom.


![pie.png](./write-up_images/pie.png)

The flag is: CSC{if_it_looks_like_the_flag_then_it_is_probably_the_flag!!!!!}

This is exactly what we came for.