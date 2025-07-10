import os
from google.genai import types


def write_file(working_directory: str, file_path: str, content) -> str:
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working direcotry'

    try:
        with open(abs_file_path, "w") as file:
            file.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except OSError as e:
        return f'Error: "{e}"'


# types.FunctionDeclaration is used to build the declartaion/schema for a function
# working_directory will be hardcoded
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write new content to the file located at the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file to run, relative to the working directory. Creates a new file if it does not exist.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written to the specified file.",
            ),
        },
    ),
)
