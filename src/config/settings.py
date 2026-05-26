import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parents[2]

ROOMS_DATA_FILE_PATH = BASE_DIR / "input data" / "rooms.json"
STUDENTS_DATA_FILE_PATH = BASE_DIR / "input data" / "students.json"

OUTPUT_FOLDER_PATH = Path(os.getenv("OUTPUT_PATH", BASE_DIR / "output data"))

OUTPUT_FORMATS_AVAILABLE = (
    os.getenv("OUTPUT_FORMATS_AVAILABLE", "json xml").lower().split()
)

SQL_SCRIPTS_FOLDER = BASE_DIR / "src" / "scripts"

DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password123")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_NAME = os.getenv("POSTGRES_DB", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", 5432)

DB_CONNECTIONS_DICT = {
    "database": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "port": DB_PORT,
}
