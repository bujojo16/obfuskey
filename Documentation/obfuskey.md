# Obfuskey

A cryptocurrency wallet seedphrase reversible, offline, trustless, password based obfuscation to end the paper-seedphrase nonsense.

or mapping finite sets with infinite sets

***

## Summary
1. Background
2. Obfuscation
3. Offset calculation
    1. Algorithm
    2. theoretical limitations
    3. Practical experiments
4. Security

***

## 1. Background

Before going deeper into the "hows", let's quickly go through the "whys". Using cryptocurrencies - *which could be summed-up as a very technologically advanced way of managing one's own funds* - it felt really stupid to have to rely on a piece of paper to safely store the only way to recover a wallet, i.e. the seedphrase. It feels paradoxal that the only way to safely store it is on a piece of paper which can be:
    - found by anybody else than you, meaning loss of control over your wallet
    - destroyed by any environmental event (would it be fire, water, earthquake ...?)
You can of course try to mitigate the second point by not using paper, some might even use metal, but if anyone else than you find your media, they get your keys, your cryptos.

Lets quickly state here that I am aware of the existence of passphrase-protected seedphrases but this doesn't solve the problem since you still should never have your seedphrase in the open even if it is protected by a passphrase.

You can of course opt for a digital storage, which is a terrible idea because, for the following reasons:
1. Digital
Because it is on the digital form, if anything happens you don't have a physical copy of it and if you are encrypting the file, you can't actually print it out, you need the bytes in the file.
2. Storage
Since it is text base, you can for example write it in a .txt file and then decide do you want to store it in a protected environment (authenticated cloud service?) but what do you do the day the service collapses or the file is lost ?
3. File type
You can choose to write it in a .txt file and then zip it adding a password. You can then store it in multiple devices. Problem: breaking an encryption is possible and can be done very efficiently with enough computing power. You could also use a specific file type designed only for this purpose but this means it can also be deleted/discontinued/etc

The main take-out is in a perfect world you would need to have it both on a physical media AND under a digital form BUT without having to rely on any third party for the storage and protection of the file WHILE keeping the physical copy not readable.

The obvious solution to this problem is obfuscation. Rendering the seedphrase useless but still having it under the form of mnemonic words so it is easy to write down on a physical media if needed as well as under a digital form.

## 2. Obfuscation

With this obfuscation, we simply re-index every word of the seedphrase into the mnemonic without keeping its original form (words spacing) by using one or more - but preferably more - password(s).

## 3. Offset calculation

The heavy lifting of this obfuscation resides within the offset calculation algorithm. The offsets are calculated from the password used to protect the seedphrase.

### 1. Algorithm

In order to calculate our offsets we are basically using only one function. This function being recursive and with variable parameters, having one of the values doesn't give us any clue about the other offset values.

Let's already clear things up a little bit. The password is only a human-machine interface used to help us remember our key to the obfuscation. The password should actually be seen as an array of unique numbers which are the Unicode code-point of the letters composing the password. Therefore, a password "abcdefg" should be interpreted as:
```python
[ord(a), ord(b), ord(c), ord(d), ord(e), ord(f), ord(g)]
```
For readability we will consider the array "pwd":
```python
pwd = [a,b,c,d,e,f,g]
```
Where a,b,c,d,e,f,g are integers.

So, in order to obfuscate, we first calculate a global password value as follow:
```python
offset = 1
for element in pwd:
    offset = element * (offset + 1)
```

Once the offset is set as a large number based on every characters of the password, we run again this algorithm but now saving each of the offset into an array the length of our seedphrase (one offset per word in the seedphrase) initialized to 0:
```python
offsetList = [] 
for i in range(seedphrase_length):
    offsetList.append(0)
for i in range(len(pwd)):
    offset = pwd[i] * (offset + 1)
    offsetList[i%seedphrase_length] = offsetList[i%seedphrase_length] + offset%prime_divisor    #We are overflowing if the password is longer than the seedphrase
```
where prime\_divisor is the first prime number bigger than our mnemonic size.

This way, we are generating a different offset even if the character is the same and the outcome is seemingly random.


### 2. Theoretical limitations

Because we are accepting any Unicode input as a password (technically an infinity of input since we don't limit the password length and there are 1114112 unicode code points per today) to generate a list of words (12, 24 maybe words) from the mnemonic (a finite set of 2048 possible words), we are mapping something very small with something very large. Because we cannot have output outside of the mnemonic set or null/zero outputs, this obviously means we will have more than one password generating the same list of offsets, therefore the same list of words. Before adding the overflow (v1.0) these duplicates were very common and defined as follow:
Given two passwords A and B of different lengths, if:
```python
 A.offset == B.offset mod prime\_divisor
```
and 
```python
A[0..12] == B[0..12]
```
then
```python
A.offsetList == B.offsetList
```

This was addressed by adding the overflow meaning if the password is longer than the seedphrase we continue to calculate offsets and adding them to the value in the position we are in the list (v2.0).

With this v2.0 we now have a lot less duplicates as you will see below in the practical examples.

While the fact that we have more than one password for one set of offsets can be seen as a bug, I prefer to see it as a feature. In the same way this clearly means that another password than the one you have set will desobfuscate your seedphrase, it also renders the attack on your obfuscated seedphrase more difficult. Anyone trying to break your password would either have to test multiple times the same seedphrase they got with a different password or keep track of the billions of seedphrase they got already (because they would face a wall of duplicates) which would slow down significantly the process. You should basically see it as "not only one password will unlock my seedphrase BUT potentially every seedphrase they will get by brute-forcing it will be a duplicate of another seedphrase already". The biggest safety-argument of this obfuscation is to make it so absurdly difficult that no one will even try.

### 3.
