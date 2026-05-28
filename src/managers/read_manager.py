from pathlib import Path

from pydantic import HttpUrl, TypeAdapter

from src.readers.google_reader import GoogleReader
from src.readers.local_reader import LocalReader


class ReadManager:
    def __init__(self, url_or_path: str | Path | HttpUrl):
        self.file_path = url_or_path
        self.file_path_type = None

    def read(self) -> None:
        url_validator = TypeAdapter(HttpUrl)

        if isinstance(self.file_path, Path):
            self._read_local()

        elif isinstance(self.file_path, str) and url_validator.validate_python(
            self.file_path
        ):
            self._read_from_url(self.file_path)

        else:
            raise ValueError("INVALID PATH OR LINK")

    def _read_local(self):
        self.file_path: Path
        return LocalReader(self.file_path).read_batch()

    def _read_from_url(self):
        self.file_path: HttpUrl
        if "google" in self.file_path.host:
            return GoogleReader(self.file_path).read()

        else:
            ...
