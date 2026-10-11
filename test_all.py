"""Полный тест проекта."""
from catalog import _get_card_color, _indicator
from styles import COLOR_HIGHLIGHT, COLOR_MAIN_BG


def run_all_tests():
    """Все тесты проекта."""
    tests = []
    # Индикатор
    tests.append((_indicator(10) == "много", "indicator(10) == много"))
    tests.append((_indicator(5) == "мало", "indicator(5) == мало"))
    tests.append((_indicator(0) == "мало", "indicator(0) == мало"))
    # Подсветка
    tests.append((_get_card_color(3) == COLOR_HIGHLIGHT,
                  "get_card_color(3) == #ff8080"))
    tests.append((_get_card_color(4) == COLOR_MAIN_BG,
                  "get_card_color(4) == #FFFFFF"))
    tests.append((_get_card_color(0) == COLOR_HIGHLIGHT,
                  "get_card_color(0) == #ff8080"))

    passed = sum(1 for ok, _ in tests if ok)
    total = len(tests)

    print("=" * 60)
    print("ПОЛНЫЙ ТЕСТ ПРОЕКТА")
    print("=" * 60)
    for ok, name in tests:
        status = "✅" if ok else "❌"
        print(f"{status} {name}")
    print("=" * 60)
    print(f"Пройдено: {passed} / {total}")


if __name__ == "__main__":
    run_all_tests()