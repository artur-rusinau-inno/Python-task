from pathlib import Path


def validate_path(value: str, folder: bool = False):
    path_value = Path(value)

    if not folder:
        if not path_value.is_file():
            raise ValueError("PATH VALIDATOR: INVALID PATH")

    return path_value
