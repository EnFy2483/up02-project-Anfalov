"""Проверка вывода полей."""
import db_products as db


def test_fields():
    """Проверяет, что все поля на месте."""
    products = db.get_all_products()
    print(f"Всего товаров: {len(products)}")

    errors = 0
    for p in products:
        if not p.name:
            print(f"❌ Товар id={p.id}: нет названия")
            errors += 1
        if p.price is None:
            print(f"❌ Товар id={p.id}: нет цены")
            errors += 1
        if p.quantity < 0:
            print(f"❌ Товар id={p.id}: отрицательное количество")
            errors += 1

    if errors == 0:
        print("✅ Все товары содержат нужные поля")
    else:
        print(f"❌ Найдено ошибок: {errors}")


def test_prices():
    """Проверяет, что у всех товаров есть цена."""
    products = db.get_all_products()
    for p in products:
        if p.price is None:
            print(f"❌ Товар id={p.id}: нет цены")
            return
    print("✅ У всех товаров есть цена")
    
def test_quantity():
    """Проверяет, что у всех товаров количество ≥ 0."""
    products = db.get_all_products()
    for p in products:
        if p.quantity < 0:
            print(f"❌ Товар id={p.id}: отрицательное количество")
            return
    print("✅ У всех товаров количество ≥ 0")


if __name__ == "__main__":
    test_fields()
    test_prices()