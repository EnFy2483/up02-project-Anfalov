"""Настройки проекта."""
from pathlib import Path

# Путь к БД относительно файла config.py
DB_PATH = Path(__file__).parent / "databases" / "db_sklad18_N.db"