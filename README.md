# obfuskey

In short, a cryptocurrency wallet seedphrase reversible, offline, trustless, password based obfuscation to end the paper-seedphrase nonsense.

## Table of content
1. How to use
2. How it works
- a. Offsetting algorythm
- b. Obfuscation multiplier
3. Passwords

## 1. How to use
### 1.1 Prerequirements
This was written using Python 3.11 and you should definitely use this version. Python 3 by itself won't work because the "match" operator was made available only around version 3.9 and the user interface uses quite a lot of case matchers.
Make sure your Python version supports case-matchers.

### 1.2 Running the program
- clone this repository or download it and unzip it somewhere.
- Open a command-line terminal
- navigate to the location of this repository
- run the following command: python main.py
- Follow the instructions
- Read the help menu, read the info menus
- Try with a fake seedphrase to see how it works and if it suits your need
- go to the output directory in the project to see the resulting file
- fine tune the resulting file to make sure you will recover your passwords

Please note it is nonsensical to run both an obfuscation and a desobfuscation on the same seedphrase
since these operations reciprocate. You should run the desobfuscation on the result of an obfuscation.

## How it works
To be properly exact, this program is not obfuscating your seedphrase but rather re-indexing it
using one or more passwords. This re-indexation can be considered an obfuscation since it renders the 
obfuscated seedphrase useless if the password is not known. The original idea was an obfuscation and
the name stuck to the project while the way of doing it became clearer. I would argue that ObfusKey
sounds a lot nicer than "Re-indexer".
### a. Offsetting algorythm
In order to obfuscate your seedphrase, we need first need to stop seeing it as a phrase made of 
words but rather a list of indexes. These indexes are going to be offset by a determinated value
based on a password in a way that they are not anymore the reflection of the original indexes.
This means that the gaps between each indexes must not be constant because offsetting the whole
seedphrase at once is not giving much of a brute-force resistance.
For example, a seedphrase like "test test test test" must not be equal to "sea sea sea sea" when
obfuscated.

To do so, we take the password entered and calculate an initial password value based on the
ordinal of each character in the ASCII table:
        for character in self.password:
            self.offset = ord(character) * (self.offset + 1)
        self.offset = self.offset%prime_divisor
We then populate an array the size of the seedphrase with offset indexes calculated as 
follow:
         for i in range(seedphrase_length):
            self.offset = ord(self.password[i%len(self.password)]) * (self.offset +1)
            self.offsetList.append(self.offset%prime_divisor)
This array is what we are going to use for both obfuscating and desobfuscating our seedphrase.

The only difference between obfuscation and desobfuscation is the sign of the operation.
When obfuscating, we add the password-generated indexes to each word index from our seedphrase.
When desobfuscating, we substract the password generated indexes to each word index from our obfuscated seedphrase.

### b.Security and Obfuscation multiplier
Considering any BIP-39 seedphrase, anybody can randomly input words in a random order and hope for the best to open any wallet. for a 24 words seedphrase using the BIP39 mnemonic, this gives us a potential 2.96x10^79 possibilities. Because this number is so gigantic, it renders this method useless.
If an attacker is targeting you and finds your seedphrase, that's it for you.
If an attacker is targeting you and finds your obfuscated seed phrase, things are a little different.

Knowing you have obfuscated it, he can try to change words in the phrase randomly. The first problem he is going to encounter is that any result is valid. Unlike an encryption that is only valid when broken, an obfuscation is always giving a valid result, the real validity then needs to be checked by an online block explorer of comparing it to the ledger of the blockchain you are using. This already makes the computing power required a tad bit higher than what it would be to simply bruteforce an encryption.

Now let's say the attacker has seen your unaltered output txt from the obfuscation and he knows that your password has at least 3 letters and the third one is X. This means he now has to first go through all possible 3 word passwords using the 85 codepoints. Then, all the possible 4 word, then all possible 5 word .. And at every step of the way, he needs to compare the result with the ledger of the blockchain to check if he got your seedphrase.

Taking that in account, if you are using a 24 characters long password, an attacker still needs to try all possible combinations of all lengths between 3 and 24, which makes it around 2x10^46.

Now, I know this is lower than the original 2.96x10^79 you are getting using all the possibilities in the mnemonic meaning it is still more interesting to attack your seed this way.

This is why we can use multiple obfuscation. By adding layers of obfuscation on top of already obfuscated seedphrases, we are actually multiplying our possibilities. Adding a second 24 characters long password and a second round of obfuscation to the process, we are now generating not 2* 2x10^46 but actually (2x10^46)^2 which means 4.09x10^92 which is now even bigger than the security provided by the 2048 words mnemonic.

If you doubt this, consider that we don't have any info on the obfuscated seedphrased between the first and the last one, meaning the attacker cannot find one first and then focus on the other one, he will have to compute simultaneously for both passwords. And if you want to spice it up more, you can add any amount of passwords.

As an example, adding twenty times the password "abcde" probably provides even more security than carefully choosing two very good 24 characters passwords. 

## 3. Passwords
In the end, the level of security this program will bring you is directly depending on the strength of your passwords. Using very generic short passwords like "password" or "hello1" etc that can be found in dictionaries or passwords listing is not going to be of any help. The only easy way of breaking this obfuscation is by running a huge compilation of generic passwords and you should make sure your password would never be found in there.

### What is a good password?
A good password is first of all not one word but several separated by unusual characters. Also, the words can be non traditional word, things you won't find in a dictionary and should definitly be with upper and lower case letters since they are not normally found with this way in dictionaries. Then, on top of that, adding very specific words or letters that tie the password to the thing you are protecting will help insure your password has never been used anywhere else. Lastly, dates, acronym, nicknames are a good addition.

A password must never be shorter than 12 characters and ideally should never be shorter than 24 characters but then again, in our case, if you stack 3 or 4 passwords on top of each other, it doesn't really matter if they are 12 or 15 characters long, they will provide safety.
