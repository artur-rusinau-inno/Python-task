# 1. Установка
---
### С помощью uv
```bash
git clone https://github.com/artur-rusinau-inno/Python-task.git
uv sync
```
### С помощью pip (серьезно? в 2026?)
```bash
git clone https://github.com/artur-rusinau-inno/Python-task.git
python -m venv .venv
.venv\scripts\activate # для Windows
source .venv/bin/activate # для Linux/Mac
pip install -r requirements.txt
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
- Поднимаем контейнер с PostgreSQL
```bash
docker-compose up -d
```
- Запуск основной программы
### UV
```bash
uv run python -m src.app --rooms path/to/file.json --students path/to/file.json --format json
```
### PIP
```bash
python -m src.app --rooms path/to/file.json --students path/to/file.json --format json
```
поле format в обоих случаях необязательно, по умолчанию используется json
