## Alien Object

### Description

> NASA requested your assistance in identifying this Alien Object


### Solution

1. Open the file cosmos.jpg with an image viewer/editor of your choice.
2. You will see a cosmic region. However, no hint where to look for the flag seems to be present, at least not at first glance.
3. Take a look at the metadata of the file. Especially, at the EXIF data.
4. You will recognize a strange value in the EXIF field with the tag ID 0xc614 (UniqueCameraModel).
5. The string looks like Base64 encoded data. Decode it with a tool/script of your choice (e. g. with this online decoder: https://www.motobit.com/util/base64-decoder-encoder.asp).
6. The decoded string starts with PK followed by some unprintable characters (hex: 50 4B 03 04). This seems to be the magic number which identifies a certain file format.
7. Safe the decoded string to a file and let the operating system decide how to open it. If the system is unable to open it, follow these steps:
    * Search for a list of file signatures on the Internet.
    * You will find a list like this: https://en.wikipedia.org/wiki/List_of_file_signatures
    * Look for the corresponding entry. It states that the file is probably a ZIP archive file.
    * Edit the file name accordingly: Change the file extension to zip.
8. Extract the content of the archive file using a compatible file archiver of your choice.
9. The only file extracted is the file f. It contains the flag we are looking for.
10. The flag is: `CSR{TH3#AL13U~ObJ3OT-W4S_succEs8fUl1Y_f0nuD-1n-T4e.C0sMOS!}`

### Flag

`CSR{TH3#AL13U~ObJ3OT-W4S_succEs8fUl1Y_f0nuD-1n-T4e.C0sMOS!}`

### Creator
Jan-Niklas Sohn

