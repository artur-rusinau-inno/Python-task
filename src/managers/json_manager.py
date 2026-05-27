import json
from pathlib import Path


class JSONManager:
    @staticmethod
    def read(file_path: Path) -> list[dict]:
        return json.loads(file_path.read_text())

    @staticmethod
    def save(new_file_path: Path, data: list[dict]) -> None:
        new_file_path.write_text(json.dumps(data, indent=4))
