
working_dir_abs = os.path.abspath(working_directory)
      
      target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

      valid_target_dir = os.path.commonpath([working_dir_abs, target_file])

      if working_dir_abs != valid_target_dir:
          return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
      
      if not os.path.isfile(target_file):
          return f'Error: File not found or is not a regular file: "{file_path}"'