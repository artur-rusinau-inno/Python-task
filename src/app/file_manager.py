import json
from pathlib import Path

import xmltodict

from src.config.settings import OUTPUT_FOLDER_PATH, OUTPUT_FORMATS_AVAILABLE


class FileManager:
    def read(self, input_path: str | Path):
        try:
            self.path = Path(input_path)
        except Exception as e:
            print("invalid path")
            raise e

        with open(self.path) as f:
            self.data: list[dict] = json.load(f)

    def _save_to_json(self, output_path: str | Path = OUTPUT_FOLDER_PATH):
        try:
            with open(Path(output_path) / "output.json", "w") as file:
                json.dump(self.data, file)

        except Exception as e:
            print("ERROR while saving via JSON format")
            raise e

    def _save_to_xml(self, output_path: str | Path = OUTPUT_FOLDER_PATH):
        try:
            with open(Path(output_path) / "output.xml", "w") as file:
                xmltodict.unparse(self.data, file)

        except Exception as e:
            print("ERROR while saving via XML format")
            raise e

    def save(
        self, output_path: str | Path = OUTPUT_FOLDER_PATH, file_format: str = "json"
    ):
        if file_format not in OUTPUT_FORMATS_AVAILABLE:
            raise RuntimeError("unknown file format")
        mapping = {"json": self._save_to_json, "xml": self._save_to_xml}

        try:
            mapping[file_format](output_path)
        except Exception as e:
            print("UNKNOWN ERROR")
            raise e


file_manager = FileManager()
