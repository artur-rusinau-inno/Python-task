import json
from pathlib import Path

import xmltodict

from src.config.settings import OUTPUT_FOLDER_PATH, OUTPUT_FORMATS_AVAILABLE


class FileManager:
    @staticmethod
    def read_path(input_path: str | Path) -> list[dict]:
        try:
            path = Path(input_path)
        except Exception as e:
            print("invalid path")
            raise e

        with open(path) as f:
            data: list[dict] = json.load(f)

        return data

    @staticmethod
    def _save_to_json(fetched_data: list[dict], file):
        json.dump(fetched_data, file, indent=4)

    @staticmethod
    def _save_to_xml(fetched_data: list[dict], file):
        mapping = "room"
        if "birthday" in fetched_data[0]:
            mapping = "student"

        xmltodict.unparse({"ALL": {mapping: fetched_data}}, file, pretty=True)

    @staticmethod
    def save(
        fetched_data: list[dict],
        output_path: str | Path = OUTPUT_FOLDER_PATH,
        file_format: str = "json",
    ):
        file_format = file_format.lower()
        if file_format not in OUTPUT_FORMATS_AVAILABLE:
            raise ValueError("unknown file format")
        mapping = {"json": FileManager._save_to_json, "xml": FileManager._save_to_xml}

        try:
            with open(Path(output_path) / f"output.{file_format}", "a") as file:
                mapping[file_format](fetched_data, file)
        except Exception as e:
            print(f'ERROR while saving via "{file_format.upper()}" format')
            raise e

    @staticmethod
    def clear_output_folder():
        try:
            if OUTPUT_FOLDER_PATH.exists():
                for item in OUTPUT_FOLDER_PATH.iterdir():
                    if item.is_file():
                        item.unlink()
        except FileNotFoundError:
            print("output folder is empty")


file_manager = FileManager()
