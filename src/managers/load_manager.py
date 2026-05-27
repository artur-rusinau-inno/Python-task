from pathlib import Path

from src.managers.json_manager import JSONManager


class LoadManager:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def read(self):
        if self.file_path.suffix == "json":
            result = JSONManager(self.file_path).read()

        else:
            raise ValueError("UNKNOWN FILE FORMAT")

        return result
