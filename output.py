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
   
    def write_output_to_file(output_file_path, password_objects_list, seedphrase, version):
        #To make it easier to tune-up the output, the password is shown fully and it is
        #up to the user to replace characters. Ideally, there would be only a couple of
        #visible characters and mostly "*".
        #Also, hints spaces added by default, user have to fill them and remove the 
        #instructions.
        display_password = ""
        hints = ""
        i = 1
        total_length = 53
        for password_object in password_objects_list:
            stars = "*" * (total_length - len(password_object.password)) 
            display_password += f"\t{i}.: {password_object.password}{stars}\n"
            hints += f"\t{i}.: <insert hint>\n"
            i +=1
        f = open(output_file_path, 'w')
        f.write("\t/!\ - REMEMBER TO REPLACE MOST OF THE PASSWORDS CHARACTERS BY ASTERISKS \"*\" AND TO \n\t\tADD THE NEEDED HINTS BELOW !!\n\n")
        f.write("\t/!\ - IDEALLY YOU SHOULD HAVE ONLY A COUPLE OF VISIBLE CHARACTERS FROM YOUR PASSWORDS\n\t\t AND YOUR HINTS SHOULD BE CLEAR TO YOU BUT CRYPTIC TO OTHERS !!\n\n")
        f.write(f"Passwords:\n{display_password}")
        f.write(f"\nHints:\n{hints}")
        f.write(f"\nObfuscated seedphrase: {' '.join(seedphrase)}")
        f.write(f"\n\nGenerated using ObfusKey v{version}\n\n")
        f.close()

