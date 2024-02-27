# ObfusKey

In short, a cryptocurrency wallet seedphrase reversible, offline, trustless, password based obfuscation to end the paper-seedphrase nonsense. Keep your seed-phrase protected and accessible anywhere, on computers and in paper without the need to hide it.

## Table of content
1. How to use  
1.1 Prerequirements  
1.2 Running the program  
2. How it works  
2.a Offsetting algorythm  
2.b Security and obfuscation multiplier  
3. Passwords  
3.a What is a good password?  
3.b What are good hints?  
4. Evolutions
5. Philantropy
  
## 1. How to use
### 1.1 Prerequirements
This was written using Python 3.11 and you should definitely use this version. Python 3 by itself won't work because the "match" operator was made available only around version 3.9 and the user interface uses quite a lot of case matchers.
Make sure your Python version supports case-matchers.

### 1.2 Running the program
- clone this repository or download it and unzip it somewhere
- open a command-line terminal
- navigate to the location of this repository
- run the following command:  
```bash
python main.py
```
- follow the instructions
- read the help menu, read the info menus
- try with a fake seedphrase to see how it works and if it suits your need
- go to the output directory in the project to see the resulting file
- fine tune the resulting file to make sure you will recover your passwords

Please note that it is nonsensical to run both an obfuscation and a desobfuscation on the same seedphrase
since these operations reciprocate. You should run the desobfuscation on the result of an obfuscation. Pressing "D" after an obfuscation will not return you your original seedphrase but will desobfuscate your original seedphrase since it is the one you have entered. This is not a bug.

## How it works
To be properly exact, this program is not obfuscating your seedphrase but rather re-indexing it
using one or more passwords. This re-indexation can be considered an obfuscation since it renders the 
obfuscated seedphrase useless if the password is not known. The original idea was an obfuscation and
the name stuck to the project while the way of doing it became clearer. I would argue that ObfusKey
sounds a lot nicer than "Re-indexer".  
In order to obfuscate your seedphrase, we first need to stop seeing it as a phrase made of 
words but rather a list of indexes. These indexes are going to be offset by a determinated value
based on a password in a way that they are not anymore the reflection of the original indexes.
This means that the gaps between each indexes must not be constant because offsetting the whole
seedphrase at once is not giving much of a brute-force resistance.  
For example, a seedphrase like "test test test test" must not be equal to "sea sea sea sea" when
obfuscated.  
For each index(word) of our seedphrase we get:
```bash
a: index of original seedphrase word in mnemonic  
b: index increment derived from first password  
c: index increment derived from second password  
..  
z: new index  
  
z = a + b + c + ... 
```
And because 3 + 5 = 7 just as much as 5 + 3 = 7, using your passwords in any order doesn't actually have any impact on the result. Both during obfuscation and desobfuscation.

When retrieving (desobfuscating) our seedphrase, we simply substract these increments from the new index which is the obfuscated seedphrase index.

### 2.a Offsetting algorythm  
To do so, we take the password entered and calculate an initial password value based on the
ordinal of each character in the ASCII table:  
```python
        self.offset = 1
        for character in self.password:
            self.offset = ord(character) * (self.offset + 1)
        self.offset = self.offset%prime_divisor
```  
We then populate an array the size of the seedphrase with offset indexes calculated as 
follow:  
```python
         for i in range(seedphrase_length):
            self.offset = ord(self.password[i%len(self.password)]) * (self.offset +1)
            self.offsetList.append(self.offset%prime_divisor)
```  
This array is what we are going to use for both obfuscating and desobfuscating our seedphrase.

The only difference between obfuscation and desobfuscation is the sign of the operation:
- When obfuscating, we add the password-generated indexes to each word index from our seedphrase.
- When desobfuscating, we substract the password generated indexes to each word index from our obfuscated seedphrase.

### 2.b Security and Obfuscation multiplier  
Considering any BIP-39 seedphrase, anybody can randomly input words in a random order and hope for the best to open any wallet. for a 24 words seedphrase using the BIP39 mnemonic, this gives us a potential 2.96x10^79 possibilities. Because this number is so gigantic, it renders this method useless.  
But if an attacker is targeting you and finds your seedphrase because it is on a piece of paper or writen down somewhere, he doesn't have to do anything else than recovering your wallet and that's it for your funds. 
If an attacker is targeting you and finds your obfuscated seed phrase, things are a little different.  
  
If he realizes you have obfuscated it, he can try to change words in the phrase randomly. The first problem he is going to encounter is that any result is valid because any arrangement of seedphrase words is a valid seedphrase. Unlike an encryption which is only giving a readable/valid output when broken, an obfuscation is always giving a valid result, the real validity then needs to be checked by an online block explorer of comparing it to the ledger of the blockchain you are using. This already makes the computing power required a tad bit higher than what it would be to simply bruteforce an encryption.  
  
Now let's say the attacker has found your obfuscation output txt-file. The only info he gets is the number of passwords and, if you haven't modified the output txt-file, he knows each passwords third character but not the password length. If he wants to try and break the obfuscation, he needs to go through all possible character for a length-three password, then a length-four password, then a length-five and so on, but for every password AT THE SAME TIME. Because the obfuscation process is not keeping any "in-between" obfuscations, he can't go breaking them one password at a time but rather every passwords at the same time, for every length, and comparing the result to the ledger to see if he found your wallet.  

To imagine the amount of possibilities, let's say you are using three 16 character passwords. Because he doesn't know the length of these passwords, he still have to check for infinitely long passwords but let's pretend he would know they are 16 characters long, it still amounts to around 4x10^92 combinaisons. This basically means he has more chances going on entering random seedphrases to recover whatever wallet would open than actually trying to break the obfuscated seedphrase he found. So if you trust the protection given by a BIP39 seedphrase, which has less potential possibilities than this obfuscation, then there is no reason why you wouldn't be comfortable with this obfuscation.  
  
This way of multiplying the obfuscations by using several passwords really helps rendering attacks useless to begin with but they are only as strong as your passwords are.  
  
## 3. Passwords  
In the end, the level of security this program will bring you is directly depending on the strength of your passwords. Using very generic short passwords like "password" or "hello1" that can be found in dictionaries or passwords listing is not going to be of any help because the only easy way of breaking this obfuscation is by running a huge compilation of generic passwords and you should make sure yours would never be found in there.  

It is of great importance to know how to craft a good password and how to create hints that only you can understand to help retrieving this password.  
  
### 3.a What is a good password?
A good password is first of all not one word but several words separated by specific characters. These words should be with both upper and lower case letters since passwords are case sensitive and these words are not normmally found in this shape in a dictionary for example. Also, the words can be non traditional word, words you have invented and that are not found in a dictionnary. Mixing languages is always a good approach as well.  
Then, on top of that, adding very specific words or letters that tie the password to the thing you are protecting will help insure your password has never been used anywhere else, uniqueness is maybe the most important of the criterias. Lastly, dates, acronym, nicknames are a good addition.  

As a general rule, you could say that a password must never be shorter than 12 characters and ideally should never be shorter than 24 characters but then again, in our case, if you stack 3 or 4 passwords on top of each other, it doesn't really matter if they are 12 or 15 characters long, they will provide safety.

### 3.b What are good hints?
The result of the obfuscation being so strong in itself, it is very important to be sure you will remember or recover your password without having it written in full form anywhere. To help you with this, you should tune-up the resulting txt-file, adding hints and sentences about your password, pin-pointing in time so the future you can actually get it back. This should be taken in consideration when creating your password so that it truely has a meaning for yourself and yourself only.
  
### 4. Evolution
Looking ahead from here, after testing it for so long and with so many different inputs, I won't be changing the calculatin algorythm and changes to the source-code should only be aesthetic or to add new features but not to modify the core code of the obfuscation since this could generate issues. You will always see the version which was used to generate your obfuscation in the output txt-file and you will always be able to retrieve this version on here but that wouldn't be very handy. I myself have obfuscated my seedphrases using this program and I don't want to make my life more difficult. In any case, you should download it and keep a copy somewhere so you can also re-use it when needed.  
  
### 5. Philantropy
I created this program for myself in the first place and after playing with it long enough I decided to make a very user-friendly interface and make it available to everyone in case it would serve others and maybe help making the crypto-space more attractive because not so scary to newcomers.
It took quite some time and I plan on sticking around to update it and help if anyone needs.  
  
If you feel like you would like to support this work, if this has helped you or if you simply want to give me a pat on the back, you can tip the project on these wallets:  
```bash
BTC: bc1q2ht2ytw5sh05fzdq9zvsc7ehc7a3hwcx8ccw30?message=tips  
DOGE: DKXmmjW3JrUxNhm6qhTXMqbzdqm9VJLMK3  
ADA: addr1q903tkzsm8tghwk34584yzf9ytmym37qfmtlkqe0qjp64t6lzhv9pkwk3wadrtg02gyj2ghkfhruqnkhlvpj7pyr42hs408mv4  
ETH: 0x4BE65213406c3559631edbf41dFE0022d1C97a0c  
DOT: 13iBEfF1m9JmTAf1WQ4KSqoWraqLLRakNu2HVut2LzzAEHs5  
```
  
Whether you do it or not, thanks for reading this and I hope this helps you as much as it has helped me getting out of the "paper-seedphrase-hell".  
  
Bujojo.
