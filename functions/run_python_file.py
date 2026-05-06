import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
  try:
    working_dir_abs = os.path.abspath(working_directory)

    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_file])

    if working_dir_abs != valid_target_dir:
      return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
      return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if not target_file.endswith(".py"):
      return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_file]

    if args is not None:
      command.extend(args)

    sub_process = subprocess.run(
      command, 
      text=True, 
      timeout=30, 
      cwd=working_dir_abs,
      capture_output=True)
    subOut = sub_process.stdout
    subErr = sub_process.stderr
    subCode = sub_process.returncode
    
    outputString = ""
    if subCode != 0:
      outputString = f"Process exited with code {subCode}"
    elif subOut == "" and subErr == "":
      outputString = "No output produced"
    else:
      outputString = f"STDOUT:{subOut} - STDERR:{subErr}"
      
    return outputString

  except Exception as e:
    return f"Error: executing Python file: {e}"


