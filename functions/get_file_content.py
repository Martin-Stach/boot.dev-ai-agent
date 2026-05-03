import os

from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
      working_dir_abs = os.path.abspath(working_directory)
      
      target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

      valid_target_dir = os.path.commonpath([working_dir_abs, target_file])

      if working_dir_abs != valid_target_dir:
          return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
      
      if not os.path.isfile(target_file):
          return f'Error: File not found or is not a regular file: "{file_path}"'

      with open(target_file, "r") as f:
          file_content_string = f.read(MAX_CHARS)
          if f.read(1): # Check for if the file is longer then MAX_CHARS
              file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

      return file_content_string
    
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'