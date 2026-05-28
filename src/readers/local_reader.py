from pathlib import Path

import ijson


class LocalReader:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def read_batch(self, batch_size: int = 100):
        with self.file_path.open("rb") as f:
            objects = ijson.items(f, "item")

            batch = []

            for obj in objects:
                batch.append(obj)
                if len(batch) >= batch_size:
                    yield batch
                    batch = []

            if batch:
                yield batch
