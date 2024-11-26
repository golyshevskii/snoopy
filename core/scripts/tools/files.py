import json
from typing import Any, Dict, Union


def read_file(path: str, mode: str = "r", is_json: bool = False) -> Union[str, Dict[str, Any]]:
    """
    Reads a file and returns its content.

    Params:
        path: The path to the file.
        mode: The mode to read the file.
        is_json: Whether the file is JSON or not.
    """
    with open(path, mode, encoding="utf-8") as file:
        if is_json:
            return json.load(file)
        return file.read()


def write_file(path: str, content: Dict[str, Any], mode: str = "w", is_json: bool = False) -> None:
    """
    Writes content to a file.

    Params:
        path: The path to the file.
        content: The content to write to the file.
        mode: The mode to write the file.
        is_json: Whether the file is JSON or not.
    """
    with open(path, mode, encoding="utf-8") as file:
        if is_json:
            json.dump(content, file)
        else:
            file.write(content)
