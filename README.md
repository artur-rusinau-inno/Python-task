# 1. Установка
---
### С помощью uv
```bash
git clone https://github.com/artur-rusinau-inno/Python-task.git
uv sync
```
### С помощью pip
```bash
git clone https://github.com/artur-rusinau-inno/Python-task.git
pip install requirements.txt
```
# 2. Настройка
---
Вы можете точечно настроить подключение к PostgreSQL, пути к файлам rooms и students, которые будут использованы по умолчанию, а также путь к папке с output data
1. Переименуйте файл .env.example на .env вручную или через команду
```bash
cp .env.example .env
```
2. Настройте переменные внутри .env

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
