import os


def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)

    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir])
    if working_dir_abs != valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    files = os.listdir(target_dir)

    result = ""
    for file in files:
        try:
          result += f"- {file}: file_size={os.path.getsize(target_dir+"/"+file)} bytes, is_dir={os.path.isdir(target_dir+"/"+file)}\n"
        except:
          return f'Error: Something went wrong while getting info from "{file}".'
        
    return result