import json
from pathlib import Path

import xmltodict

from src.config.settings import OUTPUT_FOLDER_PATH, OUTPUT_FORMATS_AVAILABLE


class FileManager:
    @staticmethod
    def read(input_path: Path) -> list[dict]:
        try:
            path = Path(input_path)
        except Exception as e:
            print("Invalid path")
            raise e

        with open(path) as f:
            data: list[dict] = json.load(f)

        return data

    @staticmethod
    def _save_to_json(fetched_data: list[dict], file):
        json.dump(fetched_data, file, indent=4, default=str)

    @staticmethod
    def _save_to_xml(fetched_data: list[dict], file):
        # mapping = "room"
        # if "birthday" in fetched_data[0]:
        #     mapping = "student"

        # xmltodict.unparse({"all": {mapping: fetched_data}}, file, pretty=True)
        xmltodict.unparse({"items": {"item": fetched_data}}, file, pretty=True)

    @staticmethod
    def save(
        fetched_data: list[dict],
        output_path: Path = OUTPUT_FOLDER_PATH,
        output_file_name: str = "output",
        output_file_format: str = "json",
    ):
        if not output_path.exists():
            output_path.mkdir(parents=True, exist_ok=True)

        file_format = output_file_format.lower()

        if file_format not in OUTPUT_FORMATS_AVAILABLE:
            raise ValueError(f'Unknown "{file_format.upper()}" format')

        mapping = {"json": FileManager._save_to_json, "xml": FileManager._save_to_xml}

        try:
            output_file = Path(output_path) / f"{output_file_name}.{output_file_format}"
            with open(output_file, "w") as file:
                mapping[file_format](fetched_data, file)
        except Exception as e:
            print(f'ERROR while saving via "{file_format.upper()}" format')
            raise e

        return output_file

    @staticmethod
    def clear_output_folder():
        try:
            if OUTPUT_FOLDER_PATH.exists():
                for item in OUTPUT_FOLDER_PATH.iterdir():
                    if item.is_file():
                        item.unlink()
        except FileNotFoundError:
            print("Output folder is empty")
