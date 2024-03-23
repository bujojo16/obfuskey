# Obfuskey

## Release notes

***

### v2.1
Previously the output file name was the sha256 hash of the original seedphrase. This being an obvious weak-point since it is possible to retrieve the original seedphrase by fully offline bruteforcing the hash, it is now up to the user to define the output file name. The default is "obfuscation.txt".
Changes made to files:
    - main.py
    - output.py

***

### v2.0
New version of the password offsets calculations algorithm now including an overflow to roll-over all the characters in the password if it is longer than the seedphrase.

Previously there was a *a lot* of different passwords generating the same output because they only needed to have the same overall offset value and contain the same X-first characters, X being the length of the seedphrase. Now with the overflow, the amount of duplicates when running "rockyou" with a 12 word seedphrase is reduced to 1: <!insert duplicates>

***

### v1.0
First version published.
