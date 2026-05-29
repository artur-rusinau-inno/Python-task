import asyncio

import typer

from src.config.settings import settings
from src.managers import DBManager, ReadManager, SaveManager
from src.utils import clean_folder
from src.validators import validate_input

app = typer.Typer()


async def pipeline(students: str, rooms: str, format: str, output: str) -> None:

    # ПРОВЕРКА ВХОДНЫХ ДАННЫХ
    students = validate_input(students)
    rooms = validate_input(rooms)

    output = validate_input(output, folder=True)

    # ЧТЕНИЕ ФАЙЛОВ
    students_generator = ReadManager(students).read()
    rooms_generator = ReadManager(rooms).read()

    # ИНИЦИАЛИЗАЦИЯ БД
    db = DBManager("postgres")
    await db.init()

    # УДАЛЕНИЕ СТАРЫХ ТАБЛИЦ
    await db.clear_data()

    # СОЗДАНИЕ НОВЫХ ТАБЛИЦ
    await db.create_tables()

    # ЗАГРУЗКА ДАННЫХ В БД
    await db.upload_data("rooms", rooms_generator)
    await db.upload_data("students", students_generator)

    # ВЫПОЛНЕНИЕ СКРИПТОВ
    coros = [db.execute_query(script.read_text(encoding="utf-8")) for script in settings.SQL_SCRIPTS_FOLDER.iterdir()]
    results = await asyncio.gather(*coros)

    # ОЧИСТКА ПАПКИ
    clean_folder(output)

    # СОХРАНЕНИЕ РЕЗУЛЬТАТА
    for result in results:
        if result:
            SaveManager(result).save(output, output_file_format=format)


@app.command()
def main(
    students: str = str(settings.STUDENTS_DATA_FILE_PATH),
    rooms: str = str(settings.ROOMS_DATA_FILE_PATH),
    format: str = "json",
    output: str = str(settings.OUTPUT_FOLDER_PATH),
) -> None:
    asyncio.run(pipeline(students, rooms, format, output))


if __name__ == "__main__":
    app()
