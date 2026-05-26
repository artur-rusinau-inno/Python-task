import asyncio
import json
import random
import string
from pathlib import Path

import xmltodict

from src.config.settings import OUTPUT_FOLDER_PATH, OUTPUT_FORMATS_AVAILABLE


class FileManager:
    def __init__(self):
        self._background_tasks = set()

    def read_json(self, input_path: Path | str) -> list[dict]:
        try:
            self.input_path: Path = Path(input_path)

        except TypeError:
            raise TypeError("INVALID PATH FORMAT")

        text: str | None = self.input_path.read_text()

        try:
            self.data: list[dict] = json.loads(
                text
            )  ############# СДЕЛАТЬ БАТЧИ ДЛЯ ЛОКАЛЬНОЙ ЗАГРУЗКИ 20 МЛН СТРОК
        except Exception as e:
            print("ERROR WHILE DESERIALIZING JSON")
            raise e

        return self.data

    def read_fetched_data(self, fetched_data: list[dict]) -> None:
        self.input_path = None
        self.data: list[dict] = fetched_data

    def save(
        self,
        output_path: Path = OUTPUT_FOLDER_PATH,
        output_file_name: str = None,
        output_file_format: str = "json",
    ) -> Path:

        if not output_path.exists():
            output_path.mkdir(parents=True, exist_ok=True)

        if not output_file_name:
            output_file_name: str = self._get_random_name()

        output_file_format: str = output_file_format.lower()

        if output_file_format not in OUTPUT_FORMATS_AVAILABLE:
            raise ValueError(f'UNKNOWN "{output_file_format.upper()}" FORMAT')

        try:
            output_file: Path = output_path / f"{output_file_name}.{output_file_format}"

            match output_file_format:
                case "json":
                    self._save_to_json(output_file)
                case "xml":
                    self._save_to_xml(output_file)
                case _:
                    raise ValueError(f'FORMAT "{output_file_format.upper()}" NOT SET')

        except Exception as e:
            print("UNKNOWN EROR")
            raise e

        return output_file

    async def clear_output_folder(self, folder_path: Path, minutes: int) -> None:
        if not folder_path.exists():
            return

        task = asyncio.create_task(self._task_for_delete(folder_path, minutes))
        self._background_tasks.add(task)
        task.add_done_callback(
            self._background_tasks.discard
        )  # add_done_callback содержит "магию" внутри, он сам подставляет таску первым аргументом в discard

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

    def _sync_deleting(self, folder_path: Path) -> None:
        for item in folder_path.iterdir():
            if not item.is_file():
                continue
            try:
                item.unlink()
            except Exception as e:
                print(f"CANNOT DELETE FILE {item.name}\n{e}")

    async def _task_for_delete(self, folder_path: Path, minutes: int) -> None:
        await asyncio.sleep(minutes * 60)
        await asyncio.to_thread(self._sync_deleting, folder_path)
