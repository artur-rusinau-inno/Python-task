from pathlib import Path
from typing import Iterator

import ijson

from src.config.settings import settings


class LocalReader:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def read_batch(self) -> Iterator[list[dict]]:
        if self.file_path.suffix == ".json":
            yield from self._read_json()
        else:
            raise ValueError("UNSUPPORTED FILE TYPE")

    def _read_json(self) -> Iterator[list[dict]]:
        with self.file_path.open("rb") as f:
            objects = ijson.items(f, "item")

            batch: list[dict] = []

            for obj in objects:
                batch.append(obj)
                if len(batch) >= settings.BATCH_SIZE:
                    yield batch
                    batch = []

            if batch:
                yield batch
