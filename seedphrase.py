class Seedphrase:
    def __init__(self, phrase):
        self.size = len(phrase)
        self.original_seedphrase = phrase
        self.obfuscated_phrase = []
        self.retrieved_phrase = []
        self.processed_phrase = []
        self.indexes = []

    def get_seedphrase_indexes(phrase, mnemonic):
        indexes = []
        for word in phrase:
            indexes.append(mnemonic.index(word))
        return indexes

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

