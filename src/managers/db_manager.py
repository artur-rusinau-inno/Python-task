from typing import Iterable, Literal

from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from src.adapters import PostgresAdapter
from src.config.settings import settings


class DBManager:
    def __init__(self, db_type: Literal["postgres"], *, test: bool = False) -> None:
        self.db_type = db_type
        self.db = None
        self.test = test

    async def init(self) -> None:
        if self.db_type == "postgres":
            self.db = PostgresAdapter(settings.test_pg_dsn if self.test else settings.pg_dsn)

        else:
            raise ValueError("UNSUPPORTED DB TYPE")

        await self.db.init()

    async def create_tables(self) -> None:
        await self.db.create_tables()

    async def execute_query(self, query: str, *args) -> list[dict]:
        return await self.db.execute_query(query, *args)

    async def clear_data(self) -> None:
        await self.db.clear_data()

    async def upload_data(self, table_name: str, data: Iterable) -> None:
        with Progress(
            SpinnerColumn(
                spinner_name="bouncingBar", finished_text=":white_check_mark:", style="yellow"
            ),  # Крутящийся спиннер в начале
            TextColumn("[progress.description]{task.description}"),  # Текст описания
            BarColumn(bar_width=40),  # Сама полоса прогресса
            TextColumn("[progress.completed]{task.completed} пачек"),  # Сколько батчей улетело
            TimeElapsedColumn(),  # Сколько времени прошло
        ) as progress:
            task_id = progress.add_task(description=f"Загрузка {table_name}", total=None)

            for d in data:
                await self.db.load_batch(table_name, d)
                progress.advance(task_id, advance=1)

            final_count = progress.tasks[task_id].completed
            progress.update(task_id, total=final_count)
