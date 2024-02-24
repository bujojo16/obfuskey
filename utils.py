import os

def check_file_exists(output_file_path):
    return os.path.isfile(output_file_path)

def get_path(first_part, second_part):
    return os.path.join(first_part, second_part)

def get_file_path(output_path, file_name): 
    return os.path.join(os.getcwd(),output_path, file_name)

def get_dir_path(directory_local_path): 
    return os.path.join(os.getcwd(), directory_local_path)
    
def make_dirs_if_needed(output_path):
    if os.path.isfile(output_path) == False:
        os.makedirs(output_path, exist_ok=True)


