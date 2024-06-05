# Obfuskey

## Release notes

***

### v2.2
Previously the output file was created with only the second character of the password visible, the rest being just asterisks ("*") which was for sure safer in a way that no trace of the passwords would be left on disk but at the same time rendering the tuning of the password to reveal only a few characters very combersome and terribly not user-friendly, which could lead up to the wrong position of the characters to be displayed. With this new version, the complete password is displayed and it is up to the user to replace most of it by asteriscs or any other character.

Changes made to files:  
    - main.py  
    - output.py  

***

### v2.1
Previously the output file name was the sha256 hash of the original seedphrase. This being an obvious weak-point since it is possible to retrieve the original seedphrase by fully offline bruteforcing the hash, it is now up to the user to define the output file name. The default is "obfuscation.txt".

Changes made to files:  
    - main.py  
    - output.py  

***

### v2.0
New version of the password offsets calculations algorithm now including an overflow to roll-over all the characters in the password if it is longer than the seedphrase.

Previously there was a *a lot* of different passwords generating the same output because they only needed to have the same overall offset value and contain the same X-first characters, X being the length of the seedphrase. Now with the overflow, the amount of duplicates when running "rockyou" with a 12 word seedphrase is reduced to 1: "gjee" gives the same result as "gjeegjee".

***

### v1.0
First version published.
