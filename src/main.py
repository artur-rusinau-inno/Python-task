from pathlib import Path

import typer
from psycopg2 import ProgrammingError

from src.app.db_manager import db_manager as db
from src.app.file_manager import FileManager
from src.config.settings import (
    ROOMS_DATA_FILE_PATH,
    SQL_SCRIPTS_FOLDER,
    STUDENTS_DATA_FILE_PATH,
)

app = typer.Typer()


@app.command()
def main(
    students: Path = STUDENTS_DATA_FILE_PATH,
    rooms: Path = ROOMS_DATA_FILE_PATH,
    format: str = "json",
) -> None:
    db.clear_data()
    FileManager.clear_output_folder()
    print("Data cleared")

    db.init_db()

    json_rooms = FileManager.read(rooms)
    json_students = FileManager.read(students)

    db.insert_rooms(json_rooms)
    print("Rooms added successfully")

    db.insert_students(json_students)
    print("Students added successfully")

    for script in SQL_SCRIPTS_FOLDER.iterdir():
        query = script.read_text()
        try:
            result = db.execute_query(query)
        except ProgrammingError:
            continue
        FileManager.save(
            result,
            output_file_name=f"{script.stem[:2]}_OUTPUT{script.stem[2:]}",
            output_file_format=format,
        )


if __name__ == "__main__":
    app()
