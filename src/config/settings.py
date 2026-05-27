from pathlib import Path
from typing import Annotated

from pydantic import StringConstraints
from pydantic_settings import BaseSettings

StrLower = Annotated[str, StringConstraints(strip_whitespace=True, to_lower=True)]


class TestDBSettings(BaseSettings):
    TEST_POSTGRES_PASSWORD: str = "test"
    TEST_POSTGRES_USER: str = "test"
    TEST_POSTGRES_DB: str = "test"
    TEST_POSTGRES_HOST: str = "localhost"
    TEST_POSTGRES_PORT: int = 5433


class DBSettings(BaseSettings):
    POSTGRES_PASSWORD: str = "password123"
    POSTGRES_USER: str = "postgres"
    POSTGRES_DB: str = "rooms_students"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parents[2]

    ROOMS_DATA_FILE_PATH: Path = BASE_DIR / "input data" / "rooms.json"
    STUDENTS_DATA_FILE_PATH: Path = BASE_DIR / "input data" / "students.json"

    OUTPUT_FOLDER_PATH: Path = BASE_DIR / "output data"

    OUTPUT_FORMATS_AVAILABLE: list[str] = ["json", "xml"]

    SQL_SCRIPTS_FOLDER: Path = BASE_DIR / "src" / "scripts"

    db_settings: DBSettings = DBSettings()
    test_db_settings: TestDBSettings = TestDBSettings()

    @property
    def pg_dsn(self):
        return (
            f"postgresql://{self.db_settings.POSTGRES_USER}:{self.db_settings.POSTGRES_PASSWORD}"
            f"@{self.db_settings.POSTGRES_HOST}:{self.db_settings.POSTGRES_PORT}/{self.db_settings.POSTGRES_DB}"
        )

    @property
    def test_pg_dsn(self):
        return (
            f"postgresql://{self.test_db_settings.TEST_POSTGRES_USER}:{self.test_db_settings.TEST_POSTGRES_PASSWORD}"
            f"@{self.test_db_settings.TEST_POSTGRES_HOST}:{self.test_db_settings.TEST_POSTGRES_PORT}/{self.test_db_settings.TEST_POSTGRES_DB}"
        )


settings = Settings()
