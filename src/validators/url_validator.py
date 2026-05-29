import httpx
from pydantic import HttpUrl, TypeAdapter


def validate_url(value: str) -> HttpUrl:
    url_parser = TypeAdapter(HttpUrl)
    url_value = url_parser.validate_python(value)

    response = httpx.head(str(url_value), follow_redirects=True)

    if response.is_success:
        return url_value
    raise ValueError("URL VALIDATOR: INVALID URL")
