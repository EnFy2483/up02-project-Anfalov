"""Тестирование алгоритма скидки."""
from datetime import datetime
from discount import calculate_price_with_discount


def run_tests():
    """Запуск расширенных тестов."""
    test_cases = [
    # (product_id, price, date, expected, comment)
    # --- Дата расчёта: 15.10.2026 → предыдущий месяц = сентябрь 2026 ---
    (1, 8500,  datetime(2026, 10, 15), 8500,  "Товар 1: заказ 05.09 → без скидки"),
    (2, 15000, datetime(2026, 10, 15), 15000, "Товар 2: заказ 10.09 → без скидки"),
    (3, 12000, datetime(2026, 10, 15), 12000, "Товар 3: заказ 20.09 → без скидки"),
    (4, 4500,  datetime(2026, 10, 15), 4500,  "Товар 4: заказ 15.09 → без скидки"),
    (5, 6000,  datetime(2026, 10, 15), 4500,  "Товар 5: заказов нет → скидка 25%"),

    # --- Дата расчёта: 15.11.2026 → предыдущий месяц = октябрь 2026 ---
    (1, 8500,  datetime(2026, 11, 15), 6375,  "Товар 1: в октябре заказов нет → скидка"),
    (2, 15000, datetime(2026, 11, 15), 15000, "Товар 2: заказ 02.10 → без скидки"),

    # --- Дата расчёта: 01.09.2026 → предыдущий месяц = август 2026 ---
    (4, 4500,  datetime(2026, 9, 1),   3375,  "Товар 4: в августе заказов нет → скидка"),
]

    print("=" * 70)
    print("РАСШИРЕННОЕ ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ")
    print("=" * 70)

    passed = 0
    for product_id, price, date, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price, date)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Товар {product_id} на {date.date()}: "
              f"{price} → {result} (ожидалось {expected}) — {comment}")

    print("=" * 70)
    print(f"Пройдено: {passed} / {len(test_cases)}")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()