from pathlib import Path


def validate_path(value: Path, folder: bool = False):
    path_value = Path(value)

    if not folder:
        if not path_value.is_file():
            raise ValueError("INVALID PATH")

    return path_value
