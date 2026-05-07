import os

from config import MAX_CHARS
from google.genai import types

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

schema_get_file_content = types.FunctionDeclaration(
name="get_file_content",
description="Gets content from files in a specified directory relative to the working directory",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="File path to the file from, relative to the working directory",
        ),
    },
  )
)