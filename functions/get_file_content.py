import os
from functions.config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory: str, file_path: str) -> str:
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory.'

    if not os.path.isfile(abs_file_path):
        f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        if os.path.getsize(abs_file_path) > MAX_CHARS:
            file_content_string += (
                f'[...File "{file_path}" truncated at 10000 characters]'
            )
        return file_content_string
    except OSError as e:
        return f"Error: {e}"


# types.FunctionDeclaration is used to build the declartaion/schema for a function
# working_directory will be hardcoded
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Outputs up to 10000 characters of content from the specified file, constrained to the working directory..",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
    ),
)
