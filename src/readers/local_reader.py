from pathlib import Path

import ijson

from src.config.settings import settings


class LocalReader:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def read_batch(self):
        if self.file_path.suffix == ".json":
            yield from self._read_json()
        else:
            raise ValueError("UNSUPPORTED FILE TYPE")

    def _read_json(self):
        with self.file_path.open("rb") as f:
            objects = ijson.items(f, "item")

            batch = []

            for obj in objects:
                batch.append(obj)
                if len(batch) >= settings.READ_BATCH_SIZE:
                    yield batch
                    batch = []

            if batch:
                yield batch
