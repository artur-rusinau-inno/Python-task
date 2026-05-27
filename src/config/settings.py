from pathlib import Path
from typing import Annotated

from pydantic import StringConstraints
from pydantic_settings import BaseSettings

StrLower = Annotated[str, StringConstraints(strip_whitespace=True, to_lower=True)]


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parents[2]

    ROOMS_DATA_FILE_PATH: Path = BASE_DIR / "input data" / "rooms.json"
    STUDENTS_DATA_FILE_PATH: Path = BASE_DIR / "input data" / "students.json"

    OUTPUT_FOLDER_PATH: Path = BASE_DIR / "output data"

    OUTPUT_FORMATS_AVAILABLE: list[str] = ["json", "xml"]

    SQL_SCRIPTS_FOLDER: Path = BASE_DIR / "src" / "scripts"

    DB_PASSWORD: str = "password123"
    DB_USER: str = "postgres"
    DB_NAME: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    DB_CONNECTIONS_DICT: dict = {
        "database": DB_NAME,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "port": DB_PORT,
    }


settings = Settings()
