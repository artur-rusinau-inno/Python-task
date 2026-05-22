from src.app.db_manager import db_manager
from src.app.file_manager import file_manager
from src.config.settings import ROOMS_DATA_FILE_PATH, STUDENTS_DATA_FILE_PATH


def main() -> None:
    db_manager.init_db()
    rooms = file_manager.read(ROOMS_DATA_FILE_PATH)
    students = file_manager.read(STUDENTS_DATA_FILE_PATH)
    db_manager.insert_rooms(rooms)
    db_manager.insert_students(students)


if __name__ == "__main__":
    main()
