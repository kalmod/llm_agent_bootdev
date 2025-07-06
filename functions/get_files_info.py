# get_files_info.py
import os


# Returns strings as this is going to be fed into our llm agent
def get_files_info(working_directory: str, directory: str | None = None) -> str:
    abs_working_dir = os.path.abspath(working_directory)

    if directory is None:
        return f'Error: "{directory}" is not a directory'
    if directory.startswith("/"):
        directory = directory[1:]

    abs_dir_path = os.path.abspath(os.path.join(working_directory, directory))

    common_path = os.path.commonpath(
        [
            abs_working_dir,
            os.path.abspath(os.path.join(working_directory, directory)),
        ]
    )

    # if directory does is not a valid directory
    if not os.path.isdir(abs_dir_path):
        return f'Error: "{directory}" is not a directory'
    # if directory does not exist inside working directory
    # if directory is the same or a subdirectory of working directory
    # the common prefix should be equal to working_directory
    if common_path != abs_working_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    return get_directory_content_info(os.path.join(abs_working_dir, directory))


def get_directory_content_info(directory: str) -> str:
    content_info = []
    contents = os.listdir(directory)
    for _, item in enumerate(contents):
        item_info = (
            f"- {item}: "
            f"file_size={os.path.getsize(os.path.join(directory, item))},"
            f" is_dir={os.path.isdir(item)}"
        )
        content_info.append(item_info)

    return "\n".join(content_info)
