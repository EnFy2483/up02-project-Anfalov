from pathlib import Path
COMPANY_NAME = "ОбувьПлюс"
DB_PATH = Path(__file__).parent /"up02_project"/ "databases" / "db_sklad18_N.db"
APP_TITLE = f"Система заказа — {COMPANY_NAME}"
FONT_FAMILY = "Calibri"
COLOR_HIGHLIGHT = "#ff8080"   # подсветка для товаров с количеством ≤3
COLOR_HEADER = "#D2F6E7"      # фон шапки каталога