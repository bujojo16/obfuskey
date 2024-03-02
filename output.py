import hashlib
import os
import utils

class Output:
    directory_path = "output"

    def create_output_file_and_write_output(seedphrase, password_list, version, output_path = directory_path):
        output_dir_path = utils.get_path(os.getcwd(), output_path)
        utils.make_dirs_if_needed(output_dir_path)
        file_name = Output.get_file_name(seedphrase.original_seedphrase)
        output_file_path = utils.get_path(output_dir_path, file_name)
        if utils.check_file_exists(output_file_path) == True:
            return {'success':False, 'message': "ABORTED - Output file already exist!"}
        Output.write_output_to_file(output_file_path, password_list, seedphrase.obfuscated_phrase, version)    
        return {'success': True, 'message': "SUCCESS - File created"}

    def check_output_already_exists(seedphrase):
        output_file_name = Output.get_output_path(seedphrase)
        exists = utils.check_file_exists(output_file_name)
        if exists == False:
            return [False, "file doesn't exist"]
        else:
            return [True, f"file {output_file_name} already exists!"]

    def get_output_path(seedphrase):
        return utils.get_file_path(Output.directory_path, Output.get_file_name(seedphrase))

    def get_file_name(seedphrase):
        return hashlib.sha256((' '.join(seedphrase)).encode('utf-8')).hexdigest() + ".txt"

    def write_output_to_file(output_file_path, password_list, seedphrase, version):
        display_password = ""
        i = 1
        for password in password_list: #TODO: maybe randomie which character to display?
            if len(password) > 2:
                visible_character = password.password[2]
            else:
                visible_character = "*"
            display_password += f"\t{i}.: **{password.password[2]}**************************\n"
            i +=1
        f = open(output_file_path, 'w')
        f.write(f"Passwords:\n {display_password}\n\nObfuscated seedphrase: {' '.join(seedphrase)}")
        f.write(f"\n\n\nGenerated using ObfusKey v{version}")
        f.close()

