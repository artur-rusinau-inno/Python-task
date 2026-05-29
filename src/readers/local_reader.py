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
            i = 1

            for obj in objects:
                batch.append(obj)
                if len(batch) >= settings.BATCH_SIZE:
                    print(f"попытка отправить батч №{i}, размер батча {len(batch)}")
                    yield batch
                    print("батч успешно отправлен\n")
                    batch = []
                    i += 1

            if batch:
                print(f"попытка отправить батч №{i}, размер батча {len(batch)}")
                yield batch
                print("батч успешно отправлен\n")

        print("ВСЕ ДАННЫЕ УСПЕШНО ОТПРАВЛЕНЫ\n")
