from pydantic import HttpUrl


class GoogleReader:
    def __init__(self, file_path: HttpUrl):
        self.file_path = file_path

    def read(self): ...
