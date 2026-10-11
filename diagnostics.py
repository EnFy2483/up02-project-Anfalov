"""Диагностика данных."""
import db_products as db


def check_data():
    """Проверяет данные на проблемы."""
    problems = []
    products = db.get_all_products()

    for p in products:
        if p.quantity < 0:
            problems.append(f"❌ id={p.id}: отрицательное количество")
        if p.price is None or p.price == 0:
            problems.append(f"⚠️ id={p.id}: нулевая цена")
        if not p.name:
            problems.append(f"⚠️ id={p.id}: пустое название")
        if not p.category:
            problems.append(f"⚠️ id={p.id}: пустая категория")

    print("=" * 60)
    print("ДИАГНОСТИКА ДАННЫХ")
    print("=" * 60)

    if not problems:
        print("✅ Данные в порядке")
    else:
        for pr in problems:
            print(pr)

    print("=" * 60)
    return problems


if __name__ == "__main__":
    check_data()