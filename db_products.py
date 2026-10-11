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


def get_products_by_category(category):
    """Возвращает список объектов Product по категории."""
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE категория = ?", (category,))
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
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


def get_products_low_stock():
    """Возвращает товары с количеством ≤ 3."""
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE количество <= 3")
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
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


def get_categories():
    """Список всех категорий."""
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT категория FROM Товар ORDER BY категория")
    categories = [row[0] for row in cur.fetchall()]
    conn.close()
    return categories


def get_product_sizes(product_id):
    """
    Возвращает список размеров для товара.

    В БД варианта 18 (электроника) поля «размер» нет —
    тогда возвращается пустой список.

    :param product_id: id товара
    :return: список размеров
    """
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    try:
        cur.execute("SELECT DISTINCT размер FROM Товар WHERE id = ?",
                    (product_id,))
        rows = cur.fetchall()
    except sqlite3.OperationalError:
        rows = []
    finally:
        conn.close()
    return [row[0] for row in rows if row[0]]


def print_products(products):
    """Выводит информацию о товарах."""
    print(f"\nВсего товаров: {len(products)}\n")
    for p in products:
        print(p.info())
        print("-" * 60)


def print_catalog_with_highlight(products):
    """Выводит каталог с подсветкой для товаров ≤3."""
    print(f"\n{'=' * 70}")
    print(f"КАТАЛОГ ({len(products)} товаров)")
    print("=" * 70)

    for p in products:
        highlight = "⚠ " if p.quantity <= 3 else "  "
        print(f"{highlight}{p.info()}")

    print("=" * 70)


# === ЗАПУСК ТОЛЬКО ПРИ ПРЯМОМ ВЫЗОВЕ ===
if __name__ == "__main__":
    products = get_all_products()
    print_catalog_with_highlight(products)