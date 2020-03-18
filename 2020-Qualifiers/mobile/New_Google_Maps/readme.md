# New Google Maps

## Description
I found this APK installed on my phone after a trip to China. I have a feeling there's a hidden message in it, can you find it?

Given: 
challenge.apk

## Solution
The file can be extracted using apktool. You will then find a db file inres/raw.

Open the file using an sqlite browser and examine the contacts. Use the first letter of the description columns to create the flag.