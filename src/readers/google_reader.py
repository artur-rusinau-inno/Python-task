import re

import httpx
import ijson
from pydantic import HttpUrl

from config.settings import settings


class GoogleDriveReader:
    def __init__(self, file_path: HttpUrl):
        self.file_path = str(file_path)
        self.access_token = settings.GOOGLE_ACCESS_TOKEN

    def extract_gdrive_id(url: str) -> str:
        match = re.search(r"/file/d/([a-zA-Z0-9_-]+)", url)
        if not match:
            raise ValueError("INVALID GOOGLE DRIVE URL")
        return match.group(1)

    async def read_batch(self):
        api_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", self.file_path) as response:
                response.raise_for_status()  # делает raise если код ответа не 200 или 300

                objects = ijson.items_async(response.aiter_bytes(), "item")

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
