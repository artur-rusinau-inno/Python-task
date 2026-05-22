# 1. Установка
---
### С помощью uv
```bash
git clone ...
uv sync
```
### С помощью pip
```bash
git clone ...
pip install requirements.txt
```
# 2. Настройка
---


# 3. Запуск
---
### С помощью uv
1) Поднимаем контейнер с PostgreSQL
```bash
docker-compose up -d
```
2) Запуск основной программы
```bash
uv run python -m src.app --rooms path/to/file.json --students path/to/file.json --format json
```
поле format необязательно, по умолчанию используется json
### С помощью pip
1) Поднимаем контейнер с PostgreSQL
```bash
docker-compose up -d
```
2) Запуск основной программы
```bash
python -m src.app --rooms path/to/file.json --students path/to/file.json --format json
```
поле format необязательно, по умолчанию используется json
