from format_colors import fabulous_print, Color
from functions.config import WORKING_DIRECTORY

from google.genai import types

from functions.get_files_info import (
    schema_get_files_info,
    get_files_info,
)
from functions.get_file_content import (
    schema_get_file_content,
    get_file_content,
)
from functions.run_python_file import (
    schema_run_python_file,
    run_python_file,
)
from functions.write_file import (
    schema_write_file,
    write_file,
)

AVAILABLE_FUNCTIONS_DICT = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def call_function(function_call_part, verbose=False) -> types.Content:
    if verbose:
        fabulous_print(
            Color.MAGENTA,
            f"Calling Function: {function_call_part.name}({function_call_part.args})",
        )
    else:
        fabulous_print(Color.MAGENTA, f" - Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    if function_call_part.name not in AVAILABLE_FUNCTIONS_DICT:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unkonwn function: {function_name}"},
                )
            ],
        )

    result = AVAILABLE_FUNCTIONS_DICT[function_name](
        WORKING_DIRECTORY, **function_call_part.args
    )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )
