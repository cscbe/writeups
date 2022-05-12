# Solution

Open PikaPad with an Android decompiler (e.g. Jadx-gui or ByteCodeViewer) and you see the following code in MainActivity:

```java
public void onDataEntered(Pinview pinview, boolean z) {
        String value = pinview.getValue();
        String substring = value.substring(0, 3);
        String substring2 = value.substring(2, 5);
        String substring3 = value.substring(4, 6);
        if (Integer.parseInt(substring) * 7 == 1918 && (Integer.parseInt(substring2) >> 3) == 52 && (Integer.parseInt(substring3) << 5) == 2208) {
            Toast.makeText(getApplicationContext(), "You caught a " + getResources().getStringArray(R.array.flags)[Integer.parseInt(substring) + Integer.parseInt(substring2) + Integer.parseInt(substring3)], 1).show();
            return;
        }
        Toast.makeText(getApplicationContext(), "Wild Pokemon fled...", 1).show();
        pinview.clearValue();
    }
```

In order for the pin (abcdef) to match, the following conditions need to hold:

* abc * 7 = 1918
* cef >> 3 = 52
* fg << 5 = 2208

Note that the substrings overlap. This means that

* abc = 1918 / 7 =  274
* cde = 52 << 3 = 416
* ef = 2208 >> 5 = 69

So the pincode becomes 2 7 4 1 6 9, which can be entered into the app to get the flag. If you do this statically, note that the correct resource is the sum of the three substrings, so 274 + 416 + 69 = 759. 

The flag is `csc{Bewear}`
