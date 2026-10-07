"""Загрузка товаров из БД в объекты класса Product."""
import sqlite3
from config import DB_PATH
from models import Product


def get_all_products():
    """Возвращает список объектов Product из БД."""
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        # Замените индексы в зависимости от вашей структуры!
        product = Product(
            product_id=row[0],
            name=row[1],
            category=row[2],
            description=row[3],
            price=row[4],
            supplier=row[5],
            quantity=row[6]
        )
        products.append(product)
    return products


def print_products(products):
    """Выводит информацию о товарах."""
    print(f"\nВсего товаров: {len(products)}\n")
    for p in products:
        print(p.info())
        print("-" * 60)


if __name__ == "__main__":
    products = get_all_products()

print_products(products)