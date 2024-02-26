from prime_calculator import PrimeCalculator as primeCalc
import utils
import hashlib

class Mnemonic:
    default_mnemonic = "BIP39-english.txt"
    default_mnemonic_directory = "Mnemonics"
    default_mnemonic_path = utils.get_path(
            utils.get_dir_path(default_mnemonic_directory), default_mnemonic)
    default_mnemonic_256hash = {
            "Linux": "2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda",
            "Windows": "to be determined",
            "Darwin": "to be determined",
            }

    def __init__(self, mnemonic_file = default_mnemonic_path):
        self.file = mnemonic_file
        self.size = 0
        self.prime = 0
        self.list = []
        self.set_list()
        self.set_size()
        self.set_prime()

    def set_list(self):
        file = open(self.file, 'r')
        for word in file.readlines():
            self.list.append(word.replace("\n", ""))
        file.close()

    def set_size(self):
        self.size = len(self.list)

    def set_prime(self):
        self.prime = primeCalc.find_prime(self.size)

    def check_default_mnemonic_exists():
        return utils.check_file_exists(Mnemonic.default_mnemonic_path)

    def check_hash_of_default_mnemonic(operating_system_name):
        return hashlib.sha256(open(Mnemonic.default_mnemonic_path, "rb").read()).hexdigest() == Mnemonic.default_mnemonic_256hash[operating_system_name]
