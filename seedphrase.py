from password import Password
from output import Output

class Seedphrase:
    def __init__(self, phrase):
        self.size = len(phrase)
        self.original_seedphrase = phrase
        self.obfuscated_phrase = []
        self.retrieved_phrase = []
        self.processed_phrase = []
        self.indexes = []

    def get_processed_phrase(self):
        return " ".join(self.processed_phrase)
    
    def get_seedphrase_indexes(phrase, mnemonic):
        indexes = []
        for word in phrase:
            indexes.append(mnemonic.index(word))
        return indexes

    def obfuscate_and_write_output_if_not_already_processed(self, password_list):
        check = Output.check_output_already_exists(self)
        if check[0] == False:
            self.obfuscate_seedphrase(password_list)
            return Output.create_output_file_and_write_output(self, password_list)
        elif check[0] == True: 
            return {'success': False, 'message': check[1]}

    def obfuscate_seedphrase(phrase, password_list):
        self.work_phrase = phrase
        self.get_seedphrase_indexes()
        for password in password_list:
            self.generate_safe_phrase(password)
            self.work_phrase = self.processed_phrase
            self.get_seedphrase_indexes()

    def desobfuscate_seedphrase(self, password_list):
        self.work_phrase = self.original_phrase
        self.get_seedphrase_indexes()
        for password in password_list:
            self.retrieve_seedphrase(password)
            self.phrase = self.processed_phrase
            self.get_seedphrase_indexes()

    def generate_safe_phrase(self, password):
        safe_phrase = []
        mnemonic_size = len(self.mnemonic)
        for index in range(self.size):
            safe_index = self.indexes[index] + password.offsetList[index]
            safe_word = self.mnemonic[safe_index%mnemonic_size]
            safe_phrase.append(safe_word)
        self.processed_phrase = safe_phrase#' '.join(safe_phrase)
        
    def retrieve_seedphrase(self, password):
        retrieved_phrase = []
        mnemonic_size = len(self.mnemonic)
        for index in range(self.size):
            retrieved_index = self.indexes[index] - password.offsetList[index]
            retrieved_word = self.mnemonic[retrieved_index%mnemonic_size]
            retrieved_phrase.append(retrieved_word)
        self.processed_phrase = retrieved_phrase#' '.join(retrieved_phrase)


    def inspect_parameters_types(seedphrase):
        return (seedphrase.inspect_size() and 
            seedphrase.inspect_mnemonic_type() and
            seedphrase.inspect_mnemonic_elements() and
            seedphrase.inspect_phrase_type())

    def inspect_size(seedphrase):
        return type(seedphrase.size) == int

    def inspect_mnemonic_type(seedphrase):
        return type(seedphrase.mnemonic) == list

    def inspect_mnemonic_elements(seedphrase):
        result = True
        for word in seedphrase.mnemonic:
            if type(word) != str:
                result = False
        return result
    
    def inspect_phrase_type(seedphrase):
        return type(seedphrase.phrase) == list

    def inspect_phrase_size(seedphrase):
        return len(seedphrase.phrase) == seedphrase.size

    def check_phrase_mnemonic(seedphrase):
        result = True
        for word in seedphrase.phrase:
            if word not in seedphrase.mnemonic:
                result = False
        return result

    def check_phrase(seedphrase):
        size_ok = Seedphrase.inspect_phrase_size(seedphrase)
        words_ok = Seedphrase.check_phrase_mnemonic(seedphrase)
        return size_ok and words_ok

