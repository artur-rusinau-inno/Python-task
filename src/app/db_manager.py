import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import execute_batch

from src.config.settings import DB_CONNECTIONS_DICT


class DBManager:
    def __init__(self, db_dict: dict[str, str | int]):
        self.connection: connection = psycopg2.connect(**db_dict)

    def init_db(self):
        result = self._execute_query("SELECT 1")
        if result:
            print("PostgreSQL connected successfully")
        else:
            raise RuntimeError("PostgreSQL connection failure")

        self._create_tables()

    # def insert_data(self, table: str, schema: str, data: list[dict]):
    #     self._execute_query(f"INSERT INTO {table} VALUES({schema})", data)

    def insert_rooms(self, rooms: list[dict] = None):
        self._insert_many(
            "INSERT INTO rooms (id, name) VALUES (%(id)s, %(name)s)", rooms
        )

    def insert_students(self, students: list[dict] = None):
        self._insert_many(
            "INSERT INTO students (birthday, id, name, room, sex) VALUES (%(birthday)s, %(id)s, %(name)s, %(room)s, %(sex)s)",
            students,
        )

    def clear_data(self):
        self._execute_query("DROP TABLE students")
        self._execute_query("DROP TABLE rooms")

    def _execute_query(self, query, vars: tuple | dict = None):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, vars)
                if cursor.description:
                    return cursor.fetchall()
                return

    def _create_tables(self):
        self._execute_query(
            "CREATE TABLE IF NOT EXISTS rooms (id INT PRIMARY KEY, name VARCHAR(255))"
        )
        self._execute_query(
            "CREATE TABLE IF NOT EXISTS students (birthday DATE, id INT PRIMARY KEY, name VARCHAR(255), room INT REFERENCES rooms(id), sex VARCHAR(1))"
        )

    def _insert_many(self, query, var_list):
        with self.connection as conn:
            with conn.cursor() as cursor:
                execute_batch(cursor, query, var_list, page_size=1000)


db_manager = DBManager(DB_CONNECTIONS_DICT)
