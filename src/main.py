import asyncio
from pathlib import Path

import asyncpg
import typer

from src.app.db_manager import db_manager as db
from src.app.file_manager import FileManager
from src.config.settings import (
    OUTPUT_FOLDER_PATH,
    ROOMS_DATA_FILE_PATH,
    SQL_SCRIPTS_FOLDER,
    STUDENTS_DATA_FILE_PATH,
)

app = typer.Typer()


async def pipeline(students: Path, rooms: Path, format: str, output: Path):
    await db.db_connect()
    await db.clear_data()
    await FileManager().clear_output_folder()
    await db.init_db()
    rooms_obj = FileManager().read_json_path(rooms)
    students_obj = FileManager().read_json_path(students)
    await db.insert_many_query("rooms", rooms_obj.data)
    await db.insert_many_query("students", students_obj.data)
    for script in SQL_SCRIPTS_FOLDER.iterdir():
        query: str = script.read_text()
        try:
            records: list[asyncpg.Record] = await db.connection.fetch(query)
            result: list[dict] = [dict(i) for i in records]

        except Exception as e:
            print(f"ERROR WHILE EXECUTING {script.name} FILE\n{e}")
            continue

        obj = FileManager().read_fetched_data(result)
        obj.save(
            output_path=output,
            output_file_name=f"{script.stem[:2]}_OUTPUT{script.stem[2:]}",
            output_file_format=format,
        )
    await db.connection.close()


@app.command()
def main(
    students: Path = STUDENTS_DATA_FILE_PATH,
    rooms: Path = ROOMS_DATA_FILE_PATH,
    format: str = "json",
    output: Path = OUTPUT_FOLDER_PATH,
) -> None:
    asyncio.run(pipeline(students, rooms, format, output))


if __name__ == "__main__":
    app()
