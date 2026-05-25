import json
import random
import string
from pathlib import Path

import xmltodict

from src.config.settings import OUTPUT_FOLDER_PATH, OUTPUT_FORMATS_AVAILABLE


def get_random_name() -> str:
    name = random.choices(string.ascii_letters, k=10)
    result = f"output_{''.join(name)}"
    return result


class FileManager:
    @staticmethod
    def read(input_path: Path) -> list[dict]:
        try:
            path = Path(input_path)
        except Exception as e:
            print("Invalid path")
            raise e

        file = path.read_text()
        data: list[dict] = json.loads(file)

        return data

    @staticmethod
    def _save_to_json(fetched_data: list[dict], output_file: Path) -> None:
        json_string = json.dumps(fetched_data, indent=4, default=str)
        output_file.write_text(json_string)

    @staticmethod
    def _save_to_xml(fetched_data: list[dict], output_file: Path) -> None:
        mapping = "room"
        if "sex" in fetched_data[0]:
            mapping = "student"
        xml_string = xmltodict.unparse({"all": {mapping: fetched_data}}, pretty=True)

        output_file.write_text(xml_string)

    @staticmethod
    def save(
        fetched_data: list[dict],
        output_path: Path = OUTPUT_FOLDER_PATH,
        output_file_name: str = None,
        output_file_format: str = "json",
    ) -> Path:
        if not output_path.exists():
            output_path.mkdir(parents=True, exist_ok=True)

        if not output_file_name:
            output_file_name = get_random_name()

        file_format = output_file_format.lower()

        if file_format not in OUTPUT_FORMATS_AVAILABLE:
            raise ValueError(f'Unknown "{file_format.upper()}" format')

        mapping = {"json": FileManager._save_to_json, "xml": FileManager._save_to_xml}

        try:
            output_file = Path(output_path) / f"{output_file_name}.{file_format}"

            mapping[file_format](fetched_data, output_file)

        except Exception as e:
            print(f'ERROR while saving via "{file_format.upper()}" format')
            raise e

        return output_file

    @staticmethod
    def clear_output_folder() -> None:
        try:
            if OUTPUT_FOLDER_PATH.exists():
                for item in OUTPUT_FOLDER_PATH.iterdir():
                    if item.is_file():
                        item.unlink()
        except FileNotFoundError:
            print("Output folder is empty")
