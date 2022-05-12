# Activator

## Author

Jeroen Beckers

## Given

* activator.apk

## Solution

The application can be installed on either an emulator or a real device, as it supports both ARM and x86 architectures.

While it is an Android application, none of the application logic can be found in the typical places (classes.dex). Since this is an application written in Flutter, the main application logic can be found in `/lib/<arch>/libapp.so`

It's possible to open this in Ghidra, but this won't give you too much information, as Dart (the underlying engine for Flutter) uses a very specific internal format.

There are some tools and resources available that allow you to examine a flutter library:

* https://blog.tst.sh/reverse-engineering-flutter-apps-part-1/
* https://github.com/ptswarm/reFlutter
* https://github.com/rscloura/Doldrums
* https://github.com/mildsunrise/darter
* https://rloura.wordpress.com/2020/12/04/reversing-flutter-for-android-wip/

Since the internal structure of the libapp.so is not stable, the tools will only work if they support the specific version of Flutter/Dart that it was developed in.

Luckily, Doldrums works on the version of the app. First, we need to extract the libapp.so file, by either using apktool or unzipping:

```
apktool d activator.apk
```

This will create a folder `activator` which contains our `libapp.so` in `activator/lib/arm64-v8a`. You can choose any architecture, but make sure it aligns with your emulator / device. 

Parsing with `Doldrums` gives us an output file:

```
python3 src/main.py ./activator/lib/arm64-v8a/libapp.so output
```

The output file contains a lot of information, but with some grepping, we can find items related to an activation key:

```
cat output | grep -i activation -A3 -B3
}

class _MyHomePageState@17046945 extends State {
    bool returnActivationKey
    int multiplier

    Null _MyHomePageState@17046945.() {
        Code at absolute offset: 0x1253c
    }

    String _getActivationKey@17046945() {
        Code at absolute offset: 0x134fbc
    }
```
Based on the resources listed at the start of this page, we know that the functions we see here are wrappers around the actual implementation. This means that in order to find the implementation of _getActivationKey, we have to look at `0x134fbc` and not `0x17046945`.

While you could open the binary in Ghidra and look for interesting code, it's much easier to solve this challenge dynamically.

By using Frida (https://frida.re) we can hook the function _getActivationKey and figure out what it return:

```
function init()
{
    
    var m = Process.findModuleByName("libapp.so"); 
    Interceptor.attach(m.base.add(0x134fbc), {
        onEnter: function(args) {
        },
        onLeave: function(retval)
        {
            console.log(retval);
        }
    });

}
setTimeout(init, 5000) 
```

Launch the app with this hook, enter a random code and click the 'Submit button' to see the returned value:

```
frida -U -f be.csc.activator -l hook.js
     ____
    / _  |   Frida 15.1.1 - A world-class dynamic instrumentation toolkit
   | (_| |
    > _  |   Commands:
   /_/ |_|       help      -> Displays the help system
   . . . .       object?   -> Display information about 'object'
   . . . .       exit/quit -> Exit
   . . . .
   . . . .   More info at https://frida.re/docs/home/
Spawned `be.csc.activator`. Use %resume to let the main thread start executing!
[SM G950F::be.csc.activator]-> %resume
[SM G950F::be.csc.activator]-> 0x761a4e3e19
```

Finally, let's dump the memory region for the obtained pointer by using `console.log(hexdump(retval))`:
```
             0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF
75bc4eb669  03 4e 00 00 00 00 00 22 00 00 00 00 00 00 00 46  .N.....".......F
75bc4eb679  44 31 38 34 2d 41 41 42 34 31 2d 43 37 39 38 45  D184-AAB41-C798E
75bc4eb689  01 33 00 00 00 00 00 00 00 00 00 00 00 51 40 04  .3...........Q@.
75bc4eb699  01 33 00 00 00 00 00 00 00 00 00 00 00 51 40 04  .3...........Q@.
75bc4eb6a9  01 33 00 00 00 00 00 00 00 00 00 00 80 48 40 04  .3...........H@.
75bc4eb6b9  01 33 00 00 00 00 00 00 00 00 00 00 80 48 40 04  .3...........H@.
75bc4eb6c9  01 33 00 00 00 00 00 00 00 00 00 00 00 4c 40 04  .3...........L@.
75bc4eb6d9  01 33 00 00 00 00 00 00 00 00 00 00 00 4c 40 04  .3...........L@.
75bc4eb6e9  05 4b 00 00 00 00 00 41 80 78 1a 76 00 00 00 0e  .K.....A.x.v....
75bc4eb6f9  00 00 00 00 00 00 00 8c 00 00 00 00 00 00 00 88  ................
75bc4eb709  00 00 00 00 00 00 00 62 00 00 00 00 00 00 00 70  .......b.......p
75bc4eb719  00 00 00 00 00 00 00 68 00 00 00 00 00 00 00 5a  .......h.......Z
75bc4eb729  00 00 00 00 00 00 00 82 00 00 00 00 00 00 00 04  ................
75bc4eb739  01 33 00 00 00 00 00 00 00 00 00 00 00 4a 40 04  .3...........J@.
75bc4eb749  01 33 00 00 00 00 00 00 00 00 00 00 00 4a 40 04  .3...........J@.
75bc4eb759  01 33 00 00 00 00 00 00 00 00 00 00 80 46 40 04  .3...........F@.
```
The code `FD184-AAB41-C798E` seems interesting, so let's try that in the app. After clicking submit, the app will show the flag: `csc{flitter_flatter_flutter}`
