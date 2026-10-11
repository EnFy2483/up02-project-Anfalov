"""Тестирование каталога."""
import db_products as db


def test_db_available():
    """Проверяет, что БД доступна."""
    try:
        products = db.get_all_products()
        return isinstance(products, list)
    except Exception as e:
        print(f"❌ БД недоступна: {e}")
        return False


def test_products_count():
    """Проверяет, что товары загружены."""
    products = db.get_all_products()
    return len(products) > 0


def test_product_fields():
    """Проверяет, что у всех товаров достаточно полей."""
    products = db.get_all_products()
    for p in products:
        # У объекта Product 7 полей: id, name, category, description,
        # price, supplier, quantity
        if not all([hasattr(p, attr) for attr in
                    ["id", "name", "category", "price", "quantity"]]):
            print(f"❌ Товар id={p.id}: не хватает полей")
            return False
    return True


def test_prices_are_numbers():
    """Проверяет, что все цены — числа."""
    products = db.get_all_products()
    for p in products:
        if not isinstance(p.price, (int, float)):
            print(f"❌ Товар id={p.id}: цена не число")
            return False
    return True


def test_quantity_not_negative():
    """Проверяет, что количество не отрицательное."""
    products = db.get_all_products()
    for p in products:
        if p.quantity < 0:
            print(f"❌ Товар id={p.id}: отрицательное количество")
            return False
    return True


def test_names_not_empty():
    """Проверяет, что у всех товаров есть название (ДЗ)."""
    products = db.get_all_products()
    for p in products:
        if not p.name:
            print(f"❌ Товар id={p.id}: пустое название")
            return False
    return True


def run_all_tests():
    """Прогон всех тестов каталога."""
    tests = [
        ("БД доступна", test_db_available),
        ("Товары загружены", test_products_count),
        ("У всех товаров нужные поля", test_product_fields),
        ("Все цены — числа", test_prices_are_numbers),
        ("Количество не отрицательное", test_quantity_not_negative),
        ("Названия не пустые", test_names_not_empty),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ КАТАЛОГА")
    print("=" * 60)

    passed = 0
    for name, func in tests:
        result = func()
        status = "✅" if result else "❌"
        if result:
            passed += 1
        print(f"{status} {name}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(tests)}")


if __name__ == "__main__":
    run_all_tests()