from pathlib import Path

from pydantic import HttpUrl, ValidationError

from src.validators.path_validator import validate_path
from src.validators.url_validator import validate_url


def validate_input(value: str, folder: bool = False) -> HttpUrl | Path:
    try:
        url_value = validate_url(value)
        return url_value

    except ValidationError:
        path_value = validate_path(value, folder)
        return path_value
