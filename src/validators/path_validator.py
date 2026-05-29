from pathlib import Path


def validate_path(value: str):
    path_value = Path(value)

    if not path_value.is_file():
        raise ValueError("INVALID PATH")
