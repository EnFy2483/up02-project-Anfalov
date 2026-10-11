"""Загрузка заказов из БД в объекты класса Order."""
import sqlite3
from config import DB_PATH
from models import Product, Order


def get_product_by_id(product_id):
    """Возвращает объект Product по id."""
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return Product(
        product_id=row[0],
        name=row[1],
        category=row[2],
        description=row[3],
        price=row[4],
        supplier=row[5],
        quantity=row[6]
    )


def get_all_orders():
    """
    Возвращает список объектов Order из БД.

    С пары 22 товары заказа лежат в Состав_заказа,
    поэтому каждая позиция — отдельный объект Order.
    """
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("""
        SELECT Заказ.id, Заказ.дата, Заказ.клиент,
               Состав_заказа.товар_id, Состав_заказа.количество
        FROM Заказ
        JOIN Состав_заказа ON Заказ.id = Состав_заказа.заказ_id
        ORDER BY Заказ.id, Состав_заказа.id
    """)
    rows = cur.fetchall()
    conn.close()

    orders = []
    for row in rows:
        product = get_product_by_id(row[3])  # row[3] = товар_id
        if product is None:
            continue
        order = Order(
            order_id=row[0],
            date=row[1],
            client=row[2],
            product=product,
            quantity=row[4]
        )
        orders.append(order)
    return orders


def print_orders(orders):
    """Выводит информацию о заказах."""
    print(f"\nВсего позиций в заказах: {len(orders)}\n")
    total_sum = 0
    for o in orders:
        print(o.info())
        print(f"  Сумма: {o.total()} руб.")
        total_sum += o.total()
        print("-" * 60)
    print(f"ИТОГО по всем заказам: {total_sum} руб.")


if __name__ == "__main__":
    orders = get_all_orders()
    print_orders(orders)
