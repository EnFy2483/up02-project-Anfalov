"""Финальная проверка перед ДЭ."""
import os


def precheck():
    """Проверка готовности к ДЭ."""
    checks = [
        (os.path.exists("resources/picture.png"), "picture.png есть"),
        (os.path.exists("resources/logo.png"), "logo.png есть"),
        (os.path.exists("resources/icon.ico"), "icon.ico есть"),
        (os.path.exists("catalog.py"), "catalog.py есть"),
        (os.path.exists("styles.py"), "styles.py есть"),
        (os.path.exists("resources.py"), "resources.py есть"),
        (os.path.exists("main_catalog.py"), "main_catalog.py есть"),
        (os.path.exists("README.md"), "README.md есть"),
        (os.path.exists("test_indicator.py"), "test_indicator.py есть"),
        (os.path.exists("test_highlight.py"), "test_highlight.py есть"),
    ]

    passed = sum(1 for ok, _ in checks if ok)
    total = len(checks)

    print("=" * 60)
    print("ПРОВЕРКА ГОТОВНОСТИ К ДЭ")
    print("=" * 60)
    for ok, name in checks:
        status = "✅" if ok else "❌"
        print(f"{status} {name}")
    print("=" * 60)
    print(f"Готовность: {passed} / {total}")

    if passed == total:
        print("🎉 Проект готов к ДЭ!")
    else:
        print("⚠️ Есть проблемы — исправьте.")


if __name__ == "__main__":
    precheck()