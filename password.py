class Password:
    def __init__(self, password): # mnemonic, seedphrase):
        self.password = password
        self.offset = 1
        self.offsetList = []
        #self.calculate_password_value(mnemonic.prime)
        #self.calculate_offsetting_list(mnemonic.prime, seedphrase.size)

    def calculate_password_value(self, prime_divisor):
        for character in self.password:
            self.offset = ord(character) * (self.offset + 1)
        self.offset = self.offset%prime_divisor
        return

    #Method only used for testing outside of scope
    def calculateOffsetingList(self):
        for i in range(14):
            #self.offsetList.append((self.offset * ord(self.password[i]))%2048)
            self.offset = ord(self.password[i]) * (self.offset +1)
            self.offsetList.append(self.offset%2053)

        return

    def calculate_offsetting_list(self, prime_divisor, seedphrase_length):
        self.offsetList = []
        for i in range(seedphrase_length):
            self.offset = ord(self.password[i%len(self.password)]) * (self.offset +1)
            self.offsetList.append(self.offset%prime_divisor)
        return
