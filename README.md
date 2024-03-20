# ObfusKey

In short, a cryptocurrency wallet seedphrase reversible, offline, trustless, password based obfuscation to end the paper-seedphrase nonsense. Keep your seed-phrase protected and accessible anywhere, on computers and on paper without the need to hide it and without fear of somebody finding it.

[TODO]: insert updated picture 

The documentation here is short and meant for a quick read to get the basics of this program. For the long version, please refer to Obfuskey.md

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
  
In order to obfuscate your seedphrase, we take the index of the words in the mnemonic and shift
their position by a value determined by the password you set. Even if your password contains the
same letters, the offset value is not going to be constant, meaning that if your seedphrase is:
```bash
test test test test
```
and your password is : "aaaa", the obfuscated seedphrase will not reflect the shape of your original
seedphrase but will be:
```bash
large lesson roast today
```
And because the obfuscation is not just based on each letters but also on the password as a whole,
you will not get the same offset with "aaaa" and with "aaaab" for example, which will give you:
```bash
trade execute brown client
```

When desobfuscating (retrieving your original seedphrase) we simply proceed in reverse, and substract
the offset.

### 2.a Offsetting algorythm  
This is the short and simplified version, for more details please consult the documentation.
To obfuscate, we take the password entered and calculate an initial password value based on the
ordinal of each character in the ASCII table as a first offset value:
```python
        offset = 1
        for character in password:
            offset = ord(character) * (offset + 1)
```  
This recursive function gives us the first offset based on the password as a whole.
Then we populate an array the size of the seedphrase with a newly calculated value based on the first
offset as follow:  
```python
         for i in range(seedphrase_length):
            offset = ord(password[i]) * (offset +1)
            self.offsetList.append(offset)
```  
This function being recurvise and using variables for each step, even having one of the offset
values won't give you indications on the rest of the offsets.
This array is what we are going to use for both obfuscating and desobfuscating our seedphrase.

The only difference between obfuscation and desobfuscation is the sign of the operation:
- When obfuscating, we add the password-generated indexes to each word index from our seedphrase.
- When desobfuscating, we substract the password generated indexes to each word index from our obfuscated seedphrase.

### 2.b Security and Obfuscation multiplier  
Because this obfuscation is using the Unicode table which contains more than 1,114,112 characters, you are not making your BIP39 seedphrase any weaker by using it. An attempt to brute-force a 20 character password using every possible Unicode characters would take so much time and resources that it isn't even necessary to talk about it. You can - and should - use complicated characters combinations, even smileys if you want to.

The real protection comes from the multiplication of the obfuscation. You can set any number of passwords to obfuscate your seedphrase. Because we only keep the last obfuscation, an attacker would need to try and break every password you are using at the same time. Finding only one password will not only be transparent to the attacker but will also not be enough since he would still have to break all other passwords, without even knowing he has found one of them.

But that's not it. Because every attemp will give you a seemingly valid seedphrase, the attacker would still need to verify the checksum is correct and then, if it is, he would need to compare it to the ledger of your blockchain to verify if he has found a valid wallet address.

In short: using three 24 character passwords that are not common words or passwords you already use for another thing will make it practically impossible to break both because of the amount of time it would take but also the amount of resources to :
- calculate the values
- calculate the checksum
- compare to the ledger  
  
And this for every single possibilities of the potential 6.54^362. This number being so gigantic, it is easier - and more likely to succeed - to simply randomize every possible seedphrases in the mnemonic.
 
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
Any change to the calculation algorithm will be added as a new version and every version will always be directly available within the program, without having to download an older version, for ease of use and security. For example, you can already choose between v1.0 and v2.0.  
However, v1.0 is now considered deprecated and should not be used to obfuscate but rather to desobfucate your seedphrase if it was obfuscated using v1.0 and then reobfuscate it using v2.0.
 
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
