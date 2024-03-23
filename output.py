import hashlib
import os
import utils

class Output:
    directory_path = "output"

    def create_output_file_and_write_output(seedphrase, password_list, output_file_path, version):
        if utils.check_file_exists(output_file_path) == True:
            return {'success':False, 'message': f"ABORTED - Output file {output_file_path} already exists!"}
        Output.write_output_to_file(output_file_path, password_list, seedphrase.obfuscated_phrase, version)    
        return {'success': True, 'message': f"SUCCESS - File {output_file_path} created"}
   
    def write_output_to_file(output_file_path, password_list, seedphrase, version):
        display_password = ""
        i = 1
        for password in password_list: #TODO: maybe randomie which character to display?
            if len(password.password) > 2:
                visible_character = password.password[2]
            else:
                visible_character = "*"
            display_password += f"\t{i}.: **{password.password[2]}**************************\n"
            i +=1
        f = open(output_file_path, 'w')
        f.write(f"Passwords:\n {display_password}\n\nObfuscated seedphrase: {' '.join(seedphrase)}")
        f.write(f"\n\n\nGenerated using ObfusKey v{version}")
        f.close()

