from pathlib import Path

from pydantic import HttpUrl

from src.readers.google_reader import GoogleReader
from src.readers.local_reader import LocalReader


class ReadManager:
    def __init__(self, url_or_path: Path | HttpUrl):
        self.file_path = url_or_path
        self.file_path_type = None

    def read(self):

        if isinstance(self.file_path, Path):
            yield from self._read_local()

        elif isinstance(self.file_path, HttpUrl):
            yield from self._read_from_url()

        else:
            raise ValueError("INVALID PATH OR URL")

    def _read_local(self):
        self.file_path: Path
        yield from LocalReader(self.file_path).read_batch()

    def _read_from_url(self):
        self.file_path: HttpUrl
        if "google" in self.file_path.host:
            yield from GoogleReader(self.file_path).read_batch()

        else:
            raise ValueError("UNSUPPORTED URL TYPE")
