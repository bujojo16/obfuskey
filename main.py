import time
import os
import utils
from mnemonic import Mnemonic
from seedphrase import Seedphrase
from password import Password
from output import Output
from obfuscator import Obfuscator

class UserInterface:
    width = 88
    version = "2.1"
    texts = {
        'main': "\n\nTo interact with this software, choose one of the actions listed by typing the letter located within the brackets [] in front of the action you want to perform and then press enter:\n\n\n \t\t[H] Help \t[O] Obfuscator \t\t[Q] Quit\n\n",
        'obfuscator': "\n\nFor a clear description of the following steps, use [I]. To proceed forward and start choosing your mnemonic, use [P]. At any input, you can quit the program using [Q] or return to the previous menu using [B].\n\n\n  \t[I] Info\t[P] Proceed\t[B] Back\t[Q] Quit\n",
        'mnemonic-setter': f"\n\nBelow is a list of the already available mnemonic files, located in the \"Mnemonics\" directory. Please, enter the number in front of the mnemonic's name to select it. \n\nIf the mnemonic you require is not in the list, feel free to add it in the directory and press Enter to update the files listing.\n\n\t\t[0..9] Select File\t[B] Back\t[Q] Quit \n\nCurrently listed files:\n",
        'seedphrase-setter': "\n\nYou will now have to enter each word of your seedphrase, in the correct order, one by one and pressing Enter between every word. When the complete seedphrase has been entered, press Enter once again without typing anything to signal the end of the seedphrase. To start entering your seedphrase, use [P].\n\n If you made a mistake, press Enter and you will be able to restart the process from scratch.\n\n\n\t\t\t[P] Proceed\t[B] Back\t[Q] Quit\n",
        'password-setter': "\n\nIn order to obfuscate your seedphrase in a reversible way, you have to set a password. The obfuscation quality and security is directly depending on the password's complexity and length.\n\nYou can use any Unicode character. A password shorter than 24 characters is not recommended. Also, in order to truely protect your seedphrase, doubling the obfuscation is recommended. You can of course add as many passwords as you wish.\n\nOnce you feel like you have enough passwords set, enter an empty password to go forward.\n\n\t[I] Info\t[C] Continue\t[B] Back\t[Q] Quit\n",
        'output-setter': "\n\nYou can now choose which action you wish to perform:\n\n\t[I] Info \t[O] Obfuscate\t[D] Desobfuscate\t[B] Back\t[Q] Quit"
    }
    headers = {
        'main': "ObfusKey v1.0",
        'privatekey': "Private Key Generator",
        'obfuscator': "Seedphrase Obfuscator",
        'mnemonic-setter': "Obfuscator - Set Mnemonic",
        'seedphrase-setter': "Obfuscator - Set Seedphrase",
        'password-setter': "Obfuscator - Set Password",
        'output-setter': "Obfuscator - Set Output",
    }
    infos = {
        'obfuscator': "This program is going to ask you three things:\n  - The mnemonic from which your seedphrase is made (usually BIP39).\n  - Your private key under the form of a seedphrase.\n  - One or more password(s) to calculate your obfuscated seedphrase. \n\nYou will then have to choose do you want to obfuscate it or desobfuscate it. \nObfuscating it will output a text file (named by hashing your original seedphrase to help avoiding processing the same seed twice) where you will find your obfuscated seedphrase as well as one character from each password. \n\nYou can freely modify this text file but keeping the number of hints on your passwords minimum is crucial for security. \n\nDesobfuscating will display your original seedphrase on the screen only and not save it to any text file for security reason. \n\nPress Enter to close this info box, \"b\" to leave the obfuscator and return to the main menu, \"q\" to quit the program.",
        'password': "The obfuscation process is using the characters in your password to offset the words of your seedphrase within the mnemonic. You can use any character from the Unicode standard so technically any character you can type here is valid. While one password is enough to decouple the obfuscated seedphrase from the original one, it doesn't provide a great brute-force resistance. Adding a second password on top significantly increases the brute-forcing resistance. In case you want to use only one password, it should be long (longer than 24 characters) and include multiple uncommon characters (,;:.-_?! etc..). On the other hand, doubling the passwords don't necessarily require both passwords to be very complicated and/or very different from one another to maintain good security. \n\nPress Enter to close this info box, \"b\" to leave the obfuscator and return to the main menu, \"q\" to quit the program.",
        'output': "Obfuscate:\n By choosing this action, your seedphrase will be obfuscated using the mnemonic and password(s). You will find a text file with the resulting obfuscated seedphrase as well as indications on your passwords in the \"Output\" directory. The name of the file is a recursive hashing of the original seedphrase over every word using the sha256 algorithm so you can easily see if you have obfuscated the same seedphrase twice by mistake. You should tune up this file, add personal hints about the passwords that only you can understand so you will for sure be able to retrieve your seedphrase.\n\nDesobfuscate:\n By choosing this action, your seedphrase will be desobfuscated using the mnemonic and password(s). The outcome will only be displayed on this screen and not saved anywhere. It is up to you to write it down to use it later on. Remember to keep your desobfuscated seedphrase safe.\n\nPress Enter to close this info box, \"b\" to leave the obfuscator and return to the main menu, \"q\" to quit the program.",
    }
        
    def __init__(self, text_length = width, version = version):
        self.text_length = text_length
        self.version = version
        self.options = {}
        self.levels = []
        
    def run_check_default_mnemonic_exists_test():
        if Mnemonic.check_default_mnemonic_exists() == False:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n\n\n\n\n")
            print("Automated system verification test cannot start !\n\n".center(UserInterface.width))
            print(format_string_to_fit("Default BIP39-english.txt mnemonic is not anymore located in Mnemonics directory, please kindly move it back there and restart the program so it can self-evaluate.", UserInterface.width))
            print("\n\n\n")
            print("Running without automated test is not safe\n\n".center(UserInterface.width))
            print("Reclone from github for safety.\n\n\n\n\n".center(UserInterface.width))
            raise Exception("DO NOT PROCEED!!!")

    def run_check_hash_of_default_mnemonic_test():
        if not Mnemonic.check_hash_of_default_mnemonic() == True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n\n\n\n\n")
            print("Automated system verification test cannot start !\n\n".center(UserInterface.width))
            print(format_string_to_fit("Default BIP39-english.txt mnemonic has been altered and is not anymore matching its original sha256 hash. Please, kindly restore it and restart the program so it can self-evaluate.", UserInterface.width))
            print("\n\n\n")
            print("Running without automated test is not safe\n\n".center(UserInterface.width))
            print("Reclone from github for safety.\n\n\n\n\n".center(UserInterface.width))
            raise Exception("DO NOT PROCEED!!!")

    def run_v1_obfuscation_test():
        test_obfuscator = Obfuscator(Mnemonic(), 24, [Password("abcdefghijkl"), Password("MNOPQRSTUVWX")])
        test_seedphrase = []
        for i in range(24):
            test_seedphrase.append("test")
        test_seed = Seedphrase(test_seedphrase)
        expected_obfuscation = ['twenty', 'trip', 'soul', 'wheel', 'sketch', 'hundred', 'useful', 'father', 'sponsor', 'guard', 'chapter', 'prefer', 'garlic', 'kid', 'erase', 'purity', 'wide', 'skull', 'reopen', 'enact', 'decline', 'treat', 'correct', 'gesture']
        if test_obfuscator.perform_obfuscation(test_seed)['success'] == True and not test_seed.obfuscated_phrase == expected_obfuscation:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n\n\n\n")
            print("Automated verification test ended in error:\n\n".center(UserInterface.width))
            print("Predefined seed didn't return expected obfuscation\n\n".center(UserInterface.width))
            print(format_string_to_fit("Automated verification test didn't succeed. If the BIP39-english.txt mnemonic has been modified or is not anymore correct, please kindly restore the original one and restart the program so it can self-evaluate. If the default mnemonic is in local \"Mnemonics\" directory, the code is corrupted and shouldn't be used", UserInterface.width))
            print("\n\n\n\n")
            print("Running without automated test is not safe\n\n".center(UserInterface.width))
            print("Reclone from github for safety.\n\n\n\n\n".center(UserInterface.width))
            raise Exception("DO NOT PROCEED!!!")
     

    def run_v2_obfuscation_test():
        test_obfuscator = Obfuscator(Mnemonic(), 12, [Password("abcdefghijklmno"), Password("JKLMNOPQRSTUVWXYZ")])
        test_seedphrase = []
        for i in range(12):
            test_seedphrase.append("test")
        test_seed = Seedphrase(test_seedphrase)
        expected_obfuscation = ['claw', 'buffalo', 'ahead', 'hybrid', 'betray', 'daring', 'brave', 'slow', 'hire', 'balance', 'pipe', 'adjust']
        if test_obfuscator.perform_obfuscation(test_seed)['success'] == True and not test_seed.obfuscated_phrase == expected_obfuscation:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n\n\n\n")
            print("Automated verification test ended in error:\n\n".center(UserInterface.width))
            print("Predefined seed didn't return expected obfuscation\n\n".center(UserInterface.width))
            print(format_string_to_fit("Automated verification test didn't succeed. If the BIP39-english.txt mnemonic has been modified or is not anymore correct, please kindly restore the original one and restart the program so it can self-evaluate. If the default mnemonic is in local \"Mnemonics\" directory, the code is corrupted and shouldn't be used", UserInterface.width))
            print("\n\n\n\n")
            print("Running without automated test is not safe\n\n".center(UserInterface.width))
            print("Reclone from github for safety.\n\n\n\n\n".center(UserInterface.width))
            raise Exception("DO NOT PROCEED!!!")

    tests = [run_check_default_mnemonic_exists_test,
                     run_check_hash_of_default_mnemonic_test,
                     run_v1_obfuscation_test,
                     run_v2_obfuscation_test,]

def format_string_to_fit(string, width):
    splitted = string.split(" ")
    result = ""
    temp = ""
    for word in splitted:
        if word != '':
            if (len(temp) + len(word)) > width:
                result += f"{temp}\n"
                temp = ""
            elif "\n" in word:
                result += temp
                temp = ""
            temp += f"{word} "
            if word == splitted[-1] and result[-len(word):-1] != word:
                result += temp
    return result

def get_current_level(session):
    return session.levels[-1]

def print_header(session):
    header_line = "----------------------------------------------------------------------------------------"
    level = get_current_level(session)
    header = UserInterface.headers[level] + f" - v{session.version}"
    print(header_line + "\n" + header.rjust(44 + int(len(header)/2)) + "\n" + header_line)

def print_text(session):
    level = get_current_level(session)
    print(format_string_to_fit(UserInterface.texts[level], UserInterface.width))

def print_seedphrase(seedphrase):
    output = ""
    temp = []
    for i in range(len(seedphrase)):
        temp.append(seedphrase[i])
        if (i+1)%6 == 0 or i == len(seedphrase)-1:
            temp = " ".join(temp)
            output += (temp.center(UserInterface.width) + "\n")
            temp = []
    return output

def main():
    session = UserInterface()
    session.seedphrase = False
    session.levels.append("main")
    state = ""
    while not state in ["exit", "q"] :
        session.version = UserInterface.version
        os.system('cls' if os.name == 'nt' else 'clear')
        print_header(session)
        print_text(session)
        print("")
        state = input("\n-> ")
        match state:
            case "O" | "o":
                state = obfuscator(session)
            case "help" | "h" | "-h":
                show_help()
                state = input("")
            case "exit" | "q" | "-q" | "Q":
                return 1
            case _:
                print(f"Invalid input: \"{state}\"") 
                time.sleep(1/2)
    return 1

def list_mnemonics():
    return os.listdir("./Mnemonics/")

def get_mnemonics():
    output = {}
    i = 1
    for file_name in list_mnemonics():
        output[str(i)] = file_name
        i += 1
    return output

def display_mnemonics():
    output = ""
    for position, mnemonic in get_mnemonics().items():
        output += f"\t[{position}] - {mnemonic}\n"
    return output

def collect_seedphrase(session):
    seedphrase_list = []
    collecting = True
    i = 1
    while collecting:
        word = input(f"-> {i}: ")
        if " " in word:
            print(f"Invalid input - can't have space in a seedphrase word. Input: \"{word}\"")
        elif word == "" and len(seedphrase_list) == 0:
            print("Please enter the first word of your seedphrase")
        elif word == "" and len(seedphrase_list) > 0:
            print(print_seedphrase(seedphrase_list))
            collecting = False
        else :
            if word in session.mnemonic.list:
                seedphrase_list.append(word)
                i += 1
            else:
                print(f"Invalid input - word \"{word}\" not found in mnemonic previously set.")
    confirm = input(format_string_to_fit("Please verify the seedphrase. If it is correct, use [C] to Continue, otherwise use [R] to restart from the first word.\n\n\t\t[C] Continue\t[R] Restart\t[B] Back\t[Q] Quit\n", UserInterface.width) + "\n-> ")
    confirming = True
    while confirming:
        match confirm:
            case "C" | "c":
                return [True, seedphrase_list]
            case "R" | "r":
                seedphrase_list = []
                i = 1
                return [False, "p"]
            case "Q" | "q":
                return [False, "exit"]
            case "B" | "b":
                return [False, "back_3"]
            case _:
                print(f"Invalid input: \"{confirm}\". Ignoring")
                confirm = input("\n-> ")
      
def seedphrase(session):
    session.levels.append("seedphrase-setter")
    state = ""
    while not state in ["exit", "q", "back_3", "b"]:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_header(session)
        print_text(session)
        if not session.seedphrase == False:
            print("")
            print("!!!! A seedphrase has already been set during this session !!!!".center(UserInterface.width))
            print("")
            print("Use [P] Proceed to decide what to do with it".center(UserInterface.width))
            print("")
            state = input("\n-> ")
        if (state == ""):
            state = input("\n-> ")
        match state:
            case "back" | "b" :
                state = "back_3"
            case "exit" | "q":
                return "exit"
            case "P" | "p":
                if session.seedphrase == False:
                    result = collect_seedphrase(session)
                    if result[0] == False:
                        state = result[1]
                    elif result[0] == True:
                        session.seedphrase = Seedphrase(result[1])
                        print("\n\t\t=> Seedphrase successfully saved.")
                        time.sleep(1)
                        state = password(session)
                else:
                    print("You have already set the following seedphrase:\n\n".center(UserInterface.width))
                    print(print_seedphrase(session.seedphrase.original_seedphrase))
                    print("\n")
                    print("Do you wish to reset it or continue with it ?\n".center(UserInterface.width))
                    print("[R] Reset\t\t[C] Continue\n".center(UserInterface.width))
                    state = input("\n->  ")
                    match state:
                        case "R" | "r":
                            state = ""
                            session.seedphrase = False
                        case "C" | "c":
                            state = password(session)
            case _:
                print(f"Invalid input: \"{state}\"") 
                time.sleep(1/2)
                state = ""
    session.levels.pop()
    return state

def password_info(session):
    text = format_string_to_fit(UserInterface.infos['password'], UserInterface.width)
    output = input(f"{text}\n\n-> ")
    return output

def set_password(session):
    password_list = []
    collecting = True
    i = 1
    while collecting:
        password = input(f"-> Password n.{i}: ")
        if password == "" and password_list == []:
            print("You need to input at least one password.")
        elif password == "":
            for index in range(i-1):
                print(f"Password n.{index+1}: {password_list[index]}".center(UserInterface.width))
            collecting = False
        else:
            password_list.append(password)
            i += 1
    print(format_string_to_fit("\nPlease verify the passwords are correct and make sure you either note them down or will easily remember them. Use [C] to continue, [A] to start again.\n\n\t\t[C] Continue \t\t\t[A] Start Again \n", UserInterface.width))
    confirm = input("-> ")
    confirming = True
    while confirming:
        match confirm:
            case "C" | "c":
                return [True, password_list]
            case "A" | "a":
                password_list = []
                i = 1
                return [False, "p"]
            case "Q" | "q":
                return [False, "exit"]
            case "B" | "b":
                return [False, "back_4"]
            case _:
                print(f"Invalid input: \"{confirm}\". Ignoring")
                confirm = input("\n-> ")

def output_info(session):
    text = format_string_to_fit(UserInterface.infos['output'], UserInterface.width)
    output = input(f"{text}\n\n-> ")
    return output

def get_file_name():
    default_name = "obfuscation.txt"
    name = input("\n\nPlease enter a name for the output file. Entering an empty string will default to \n\"obfuscation.txt.\". It is recommended to use the name of your wallet so you can\n find it later on.\n\n-> ")
    if name in ["", ".txt"]:
        name = default_name
    elif len(name) < 5 or name[-4:].lower() != ".txt":
            name += ".txt"
    return name

def output(session):
    session.levels.append("output-setter")
    session.obfuscator = Obfuscator(session.mnemonic, session.seedphrase.size, session.password_list, session.version[0])
    state = ""
    while not state in ["exit", "q", "back_5", "b"]:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_header(session)
        print_text(session)
        state = input("\n-> ")
        match state:
            case "info" | "i" | "I":
                state = output_info(session)
                if state in ["b", "B"]:
                    state = "back_5"
            case "back" | "b" | "B" :
                state = "back_5"
            case "exit" | "q" | "Q":
                return "exit"
            case "D" | "d" :
                print(format_string_to_fit("Here is your desobfuscated seedphrase. It will not be writen to disk so note it down yourself if you need it. Press enter to stop displaying it.\n\n", UserInterface.width))
                print(print_seedphrase(session.obfuscator.desobfuscate_seedphrase(session.seedphrase.original_seedphrase)))
                input("Press Enter to continue")
                state = ""
            case "O" | "o" :
                output_file_name = get_file_name()
                output_dir_path = utils.get_path(os.getcwd(), "output") 
                utils.make_dirs_if_needed(output_dir_path)
                output_file_path = utils.get_path(output_dir_path, output_file_name)
                result = session.obfuscator.perform_obfuscation(session.seedphrase)
                success = result['success']
                saved_to_file = False
                if success == False:
                    pause = input("Obfuscation unsuccessful - Press Enter to return".center(UserInterface.width))
                    state = "back_5"
                elif success == True:
                    print(format_string_to_fit(str(result), UserInterface.width))
                    writing_to_output = True
                    while writing_to_output:
                        file_already_exists = utils.check_file_exists(output_file_path)
                        if file_already_exists == True:
                            print(f"\nCannot create output file - file {output_file_name} already exists!".center(UserInterface.width))
                            confirm = input(f"\n\nPlease, remove file and use [R] to retry. \n\n\t[R] Retry\t\t [B] Back\t\t[Q] Quit\n\n-> ")
                            match confirm:
                                case "R" | "r":
                                    print("Retrying...")
                                case "Q" | "q":
                                    return "exit"
                                case "b" | "back":
                                    state = "back_5"
                                    writing_to_output = False
                        elif file_already_exists == False:
                            writing_to_output = False #writing will be succesful so we don't have to keep trying
                            file_writing = Output.create_output_file_and_write_output(session.seedphrase, session.password_list, output_file_path, session.version)
                            saved_to_file = file_writing['success']
                            print(format_string_to_fit(str(file_writing), UserInterface.width)) 
                    if saved_to_file:
                        confirming = True
                        while confirming:
                            print(format_string_to_fit("A validation test on your obfuscated seedphrase returned your original seedphrase. The process is successful and the output file has now been created in the subdirectory /Output/.\n\n\n\t\t\t[B] Back \t\t[Q] Quit", UserInterface.width))
                            state = input("\n-> ")
                            match state:
                                case "Q" | "q":
                                    return "exit"
                                case "B" | "b":
                                    state = ""
                                    confirming = False
                                case _:
                                    print(f"Invalid input: \"{state}\", ignoring.")
                    else:
                        confirming = True
                        while confirming:
                            print(format_string_to_fit("Obfuscation was performed and tested successfully but writing the output file couldn't be done.\n\n\t\t\t[B] Back\t\t\t [Q] Quit \n\n -> ", UserInterface.width))
                            state = input("-> ")
                            match state:
                                case "Q" | "q":
                                    return "exit"
                                case "B" | "b":
                                    state = ""
                                    confirming = False
                                case _:
                                    print(f"Invalid input: \"{state}\", ignoring.")
    session.levels.pop()
    return state

def password(session): 
    session.levels.append("password-setter")
    state = ""
    while not state in ["exit", "q", "back_4", "b"]:
        session.password_list = []
        os.system('cls' if os.name == 'nt' else 'clear')
        print_header(session)
        print_text(session)
        state = input("\n-> ")
        match state:
            case "info" | "i" | "I":
                state = password_info(session)
                if state in ["b", "B"]:
                    state = "back_4"
            case "back" | "b" | "B" :
                state = "back_4"
            case "exit" | "q" | "Q":
                return "exit"
            case "continue" | "C" | "c":
                result = set_password(session)
                if result[0] == False:
                    state = ""
                elif result[0] == True:
                    for password in result[1]:
                        session.password_list.append(Password(password))
                    print("Password(s) successfully set")
                    time.sleep(1/2)
                    state = output(session)

            case _:
                print(f"Invalid input: \"{state}\"") 
                time.sleep(1/2)
    session.levels.pop()
    return state

def mnemonic(session):
    session.levels.append("mnemonic-setter")
    state = ""
    while not state in ["exit", "q", "back_2", "b"]:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_header(session)
        print_text(session)
        print(display_mnemonics())
        mnemonics = get_mnemonics()
        state = input("\n-> ")
        match state:
            case "back" | "b" :
                state = "back_2"
            case "exit" | "q":
                return "exit"
        if state in list(mnemonics.keys()):
            path = utils.get_path(utils.get_dir_path("Mnemonics"), mnemonics[state])    # mnemonics files are located there
            if not utils.check_file_exists(path):                                       # we check in case it doesn't exist anymore
                print("Error: The file doesn't exist.")
                time.sleep(1)
                state = ""
            else:
                session.mnemonic = Mnemonic(path)
                state = seedphrase(session) 
    session.levels.pop()
    return state

def obfuscator_info(session):
    text = format_string_to_fit(UserInterface.infos['obfuscator'], UserInterface.width)
    output = input(f"{text}\n\n-> ")
    return output

def select_version(session):
    print(format_string_to_fit(f"\n\nYou can choose which version you wish to use. The default is latest version, v{UserInterface.version} and it is recomended to use it. \n\nPlease choose which version to use between version 1.0 and {UserInterface.version}. Note that version 1.0 is considered deprecated but will always be available. If your obfuscation was performed using version 1.0, it is recommended to reobfuscate with version {UserInterface.version}.\n\n\t\t [1] Version 1.0 \t\t [2] Version {UserInterface.version}", UserInterface.width))
    version = ""
    while version not in ["1.0", UserInterface.version]:
        version = input("\n\n-> ")
        match version:
            case "1":
                version = "1.0"
            case "2":
                version = UserInterface.version
            case "q" | "Q":
                return "exit"
            case "b" | "B":
                return "back_1"
            case _:
                print("Invalid input - ignoring")
                time.sleep(1/2)
    session.version = version
    return

def run_e2e_tests():
    for test in UserInterface.tests:
        test()

def obfuscator(session):
    session.levels.append("obfuscator")
    run_e2e_tests()
    select_version(session)
    state = ""
    while not state in ["exit", "q", "back_1", "b"]:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_header(session)
        print_text(session)
        state = input("\n\n-> ")
        print("")
        match state:
            case "info" | "i" | "I":
                state = obfuscator_info(session)
                if state in ["b", "B"]:
                    state = "back_1"
            case "back" | "b" | "B" :
                state = "back_1"
            case "exit" | "q" | "Q":
                return "exit"
            case "proceed" | "P" | "p":
                state = mnemonic(session)
            case _:
                print(f"Invalid input: \"{state}\"") 
                time.sleep(1/2)
    session.levels.pop()
    return state

def show_help():
    print(format_string_to_fit("This program is meant for cryptocurrency wallet seedphrase obfuscation and recovery from said obfuscation. At every menu you can always type \"q\" and press enter to exit the program. \n\nSeedphrases and passwords are never written to disk or anywhere, no communication with any other software is made and no connection to internet is established.\n\n\t\t\tPress enter to close this menu.", UserInterface.width))
    return "start"

if __name__ == '__main__':
    main()
