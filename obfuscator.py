from seedphrase import Seedphrase

class Obfuscator:
    def __init__(self,mnemonic, seedphrase_size, password_list, version = 2):
        self.mnemonic = mnemonic
        self.seedphrase_size = seedphrase_size
        self.password_list = password_list
        if version == "1":
            self.set_passwords_parameters_v1()
        else:
            self.set_passwords_parameters_v2()

    def set_passwords_parameters_v1(self):
        for password in self.password_list:
            password.calculate_password_value(self.mnemonic.prime)
            password.calculate_offsetting_list_to_seed_size(self.mnemonic.prime, self.seedphrase_size)
 
    def set_passwords_parameters_v2(self):
        for password in self.password_list:
            password.calculate_password_value(self.mnemonic.prime)
            if (len(password.password) > self.seedphrase_size):
                password.calculate_offsetting_list_to_password_size(self.mnemonic.prime, self.seedphrase_size)
            else:
                password.calculate_offsetting_list_to_seed_size(self.mnemonic.prime, self.seedphrase_size)
    
    def perform_obfuscation(self, seedphrase):
        seedphrase.obfuscated_phrase = self.obfuscate_seedphrase(seedphrase.original_seedphrase)
        if seedphrase.original_seedphrase == self.desobfuscate_seedphrase(seedphrase.obfuscated_phrase):
            return {'success': True, 'message': 'Obfuscation is successful and desobfuscation tested successfully.'}
        else:
            return {'success': False, 'message': 'Obfuscation was not successful.'}

    def obfuscate_seedphrase(self, phrase):
        work_phrase = phrase
        for password in self.password_list:
            work_phrase = Obfuscator.generate_safe_phrase(self, work_phrase, password)
        return work_phrase

    def desobfuscate_seedphrase(self, phrase):
        work_phrase = phrase
        for password in self.password_list:
            work_phrase = Obfuscator.retrieve_original_seedphrase(self, work_phrase, password)
        return work_phrase

    def generate_safe_phrase(self, phrase, password):
        safe_phrase = []
        indexes = Seedphrase.get_seedphrase_indexes(phrase, self.mnemonic.list)  
        for index in range(len(phrase)):
            safe_index = indexes[index] + password.offsetList[index]
            safe_word = self.mnemonic.list[safe_index%self.mnemonic.size]
            safe_phrase.append(safe_word)
        return safe_phrase

    def retrieve_original_seedphrase(self, phrase, password):
        retrieved_phrase = []
        indexes = Seedphrase.get_seedphrase_indexes(phrase, self.mnemonic.list)
        for index in range(len(phrase)):
            retrieved_index = indexes[index] - password.offsetList[index]
            retrieved_word = self.mnemonic.list[retrieved_index%self.mnemonic.size]
            retrieved_phrase.append(retrieved_word)
        return retrieved_phrase


