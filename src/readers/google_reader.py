import gzip
import re
from typing import Iterator

import ijson
import requests
from pydantic import HttpUrl

from src.config.settings import settings
from src.utils import batch


class GoogleDriveReader:
    def __init__(self, file_path: HttpUrl):
        self.file_path = str(file_path)
        self.access_token = settings.GOOGLE_ACCESS_TOKEN

    @staticmethod
    def get_google_object_id(url: str) -> str:
        match = re.search(r"/file/d/([a-zA-Z0-9_-]+)", url)
        if not match:
            raise ValueError("INVALID GOOGLE DRIVE URL")
        return match.group(1)

    def read_batch(self) -> Iterator[list[dict]]:
        api_url = f"https://www.googleapis.com/drive/v3/files/{self.get_google_object_id(self.file_path)}?alt=media"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        response = requests.get(api_url, headers=headers, stream=True)
        response.raise_for_status()  # делает raise если код ответа не 200 или 300,

        if response.headers.get("Content-Encoding") == "gzip":
            clean_stream = gzip.GzipFile(fileobj=response.raw)
        else:
            clean_stream = response.raw

        objects = ijson.items(clean_stream, "item")

        yield from batch(objects)
