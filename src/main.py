import asyncio
from pathlib import Path

import typer
from pydantic import HttpUrl

from src.config.settings import settings
from src.managers import DBManager, ReadManager, SaveManager
from src.validators import validate_input

app = typer.Typer()


async def pipeline(students: Path | HttpUrl, rooms: Path | HttpUrl, format: str, output: Path) -> None:

    # ПРОВЕРКА ВХОДНЫХ ДАННЫХ
    students = validate_input(students)
    rooms = validate_input(rooms)

    # ЧТЕНИЕ ФАЙЛОВ
    students_generator = ReadManager(students).read()
    rooms_generator = ReadManager(rooms).read()

    # ИНИЦИАЛИЗАЦИЯ БД
    db = DBManager("postgres")
    await db.init()

    # ЗАГРУЗКА ДАННЫХ В БД
    await db.upload_data("rooms", rooms_generator)
    await db.upload_data("students", students_generator)

    # ВЫПОЛНЕНИЕ СКРИПТОВ
    coros = [db.execute_query(script.read_text()) for script in settings.SQL_SCRIPTS_FOLDER.iterdir()]
    results = await asyncio.gather(*coros)

    # СОХРАНЕНИЕ РЕЗУЛЬТАТА
    for result in results:
        SaveManager(result).save(output, output_file_format=format)


@app.command()
def main(
    students: str = settings.STUDENTS_DATA_FILE_PATH,
    rooms: str = settings.ROOMS_DATA_FILE_PATH,
    format: str = "json",
    output: Path = settings.OUTPUT_FOLDER_PATH,
) -> None:
    asyncio.run(pipeline(students, rooms, format, output))


if __name__ == "__main__":
    app()
