import json
import random
import string
from pathlib import Path

import xmltodict

from src.config.settings import settings


class SaveManager:
    def __init__(self, data: list[dict]):
        self.data = data

    def save(
        self,
        output_path: Path = settings.OUTPUT_FOLDER_PATH,
        output_file_format: str = "json",
    ) -> Path:

        if not output_path.exists():
            output_path.mkdir(parents=True, exist_ok=True)

        output_file_format: str = output_file_format.lower()

        if output_file_format not in settings.OUTPUT_FORMATS_AVAILABLE:
            raise ValueError(f'UNSUPPORTED "{output_file_format.upper()}" FORMAT')

        try:
            output_file: Path = output_path / f"{self._get_random_name()}.{output_file_format}"

            match output_file_format:
                case "json":
                    self._save_to_json(output_file)
                case "xml":
                    self._save_to_xml(output_file)
                case _:
                    pass

        except Exception as e:
            print("UNKNOWN EROR")
            raise e

        return output_file

    @staticmethod
    def _get_random_name() -> str:
        symbols = string.ascii_letters + string.digits
        name: list[str] = random.choices(symbols, k=10)
        result: str = f"output_{''.join(name)}"
        return result

    def _save_to_json(self, output_file: Path) -> None:
        json_string = json.dumps(self.data, indent=4, default=str)
        output_file.write_text(json_string)

    def _save_to_xml(self, output_file: Path) -> None:
        xml_string = xmltodict.unparse({"items": {"item": self.data}}, pretty=True)
        output_file.write_text(xml_string)
