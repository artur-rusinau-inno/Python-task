from pathlib import Path


def clean_folder(path: Path):
    for item in path.iterdir():
        try:
            if item.is_file():
                item.unlink()

        except FileNotFoundError:
            print(f"FOLDER CLEANER: CANNOT DELETE {item.name}")
