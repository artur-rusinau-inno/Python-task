import requests
from pydantic import HttpUrl, TypeAdapter


def validate_url(value: str) -> HttpUrl:
    url_parser = TypeAdapter(HttpUrl)
    url_value = url_parser.validate_python(value)

    response = requests.head(str(url_value), allow_redirects=True)

    if response.ok:
        return url_value
    raise ValueError("URL VALIDATOR: INVALID URL")
