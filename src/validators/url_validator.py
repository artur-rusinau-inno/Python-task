import httpx
from pydantic import HttpUrl, TypeAdapter, ValidationError


def validate_url(value: str) -> HttpUrl:
    url_parser = TypeAdapter(HttpUrl)
    url_value = url_parser.validate_python(value)

    response = httpx.head(url_value)

    if response.status_code == 200:
        return url_value
    raise ValidationError("INVALID URL")
