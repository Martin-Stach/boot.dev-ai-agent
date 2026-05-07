import os
import subprocess

from google.genai import types

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

schema_run_python_file = types.FunctionDeclaration(
name="run_python_file",
description="Runs a python file in a specified directory relative to the working directory",
parameters=types.Schema(
  required=["file_path"],
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="File path to the file from, relative to the working directory",
        ),
        "args": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(type=types.Type.STRING),
            description="Additional arguments for calling the running the file. Default is None",
      )
    }
  )
)
