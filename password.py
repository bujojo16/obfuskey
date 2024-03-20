class Password:
    def __init__(self, password):
        self.password = password
        self.offset = 1
        self.offsetList = []

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

    def calculate_offsetting_list_to_password_size(self, prime_divisor, seedphrase_length):
        self.offsetList = []
        #first we initialize our array with zeroes
        for i in range(seedphrase_length):
            self.offsetList.append(0)
        #then we add our password offsets with an overflow
        for i in range(len(self.password)):
            self.offset = ord(self.password[i]) * (self.offset +1)
            self.offsetList[i%seedphrase_length] = self.offsetList[i%seedphrase_length] + self.offset%prime_divisor
        return

    def calculate_offsetting_list_to_seed_size(self, prime_divisor, seedphrase_length):
        self.offsetList = []
        for i in range(seedphrase_length):
            self.offset = ord(self.password[i%len(self.password)]) * (self.offset +1)
            self.offsetList.append(self.offset%prime_divisor)
        return
