import asyncio
from pathlib import Path
from typing import Annotated

import typer
from pydantic import HttpUrl, TypeAdapter

from src.config.settings import settings
from src.managers.db_manager import DBManager
from src.managers.read_manager import ReadManager
from src.managers.save_manager import SaveManager

app = typer.Typer()


def url_parser(url: str) -> HttpUrl:
    return TypeAdapter(HttpUrl).validate_python(url)


async def pipeline(students: Path | HttpUrl, rooms: Path | HttpUrl, format: str, output: Path):
    # ЧТЕНИЕ ОРИГИНАЛЬНЫХ ФАЙЛОВ
    students_generator = ReadManager(students).read()
    rooms_generator = ReadManager(rooms).read()

    # ИНИЦИАЛИЗАЦИЯ БД
    db = DBManager("postgres")
    await db.init()

    # ЗАГРУЗКА ДАННЫХ В БД
    await db.upload_data(students_generator)
    await db.upload_data(rooms_generator)

    # ВЫПОЛНЕНИЕ СКРИПТОВ
    coros = [db.execute_query(script.read_text()) for script in settings.SQL_SCRIPTS_FOLDER.iterdir()]
    results = await asyncio.gather(*coros)

    # СОХРАНЕНИЕ РЕЗУЛЬТАТА
    for result in results:
        SaveManager(result).save(output, output_file_format=format)


@app.command()
def main(
    students: Path | Annotated[HttpUrl, typer.Argument(parser=url_parser)] = settings.STUDENTS_DATA_FILE_PATH,
    rooms: Path | Annotated[HttpUrl, typer.Argument(parser=url_parser)] = settings.ROOMS_DATA_FILE_PATH,
    format: str = "json",
    output: Path = settings.OUTPUT_FOLDER_PATH,
) -> None:
    asyncio.run(pipeline(students, rooms, format, output))


if __name__ == "__main__":
    app()
