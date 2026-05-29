from pathlib import Path

from pydantic import HttpUrl, ValidationError

from src.validators.path_validator import validate_path
from src.validators.url_validator import validate_url


def validate_input(value: str) -> HttpUrl | Path:
    try:
        url_value = validate_url(value)
        return url_value

    except ValidationError:
        path_value = validate_path(value)
        return path_value
