from src.app.db_manager import db_manager as db
from src.app.file_manager import file_manager
from src.config.settings import (
    ROOMS_DATA_FILE_PATH,
    SQL_SCRIPTS_FOLDER,
    STUDENTS_DATA_FILE_PATH,
)

sql_script_names = [" "]


def main() -> None:
    db.clear_data()
    file_manager.clear_output_folder()
    print("data cleared")

    db.init_db()

    rooms = file_manager.read_path(ROOMS_DATA_FILE_PATH)
    students = file_manager.read_path(STUDENTS_DATA_FILE_PATH)

    db.insert_rooms(rooms)
    print("rooms added successfully")

    db.insert_students(students)
    print("students added successfully")

    for script in SQL_SCRIPTS_FOLDER.iterdir():
        with open(script) as file:
            query = file.read()
            try:
                result = db._execute_query(query)
                file_manager.save(result, file_format="xml")
            except Exception:
                continue


if __name__ == "__main__":
    main()
