"""Обработка исключений."""
from tkinter import messagebox


def safe_call(func, *args, **kwargs):
    """
    Безопасный вызов функции.

    Ловит типичные ошибки и показывает окна сообщений.
    Возвращает результат func или None при ошибке.

    :param func: вызываемая функция
    :param args: позиционные аргументы
    :param kwargs: именованные аргументы
    :return: результат func или None
    """
    try:
        return func(*args, **kwargs)
    except FileNotFoundError as e:
        messagebox.showerror("Файл не найден", str(e))
    except ConnectionError as e:
        messagebox.showerror("Ошибка соединения", str(e))
    except ValueError as e:
        messagebox.showwarning("Неверное значение", str(e))
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))
    return None


def validate_positive_int(value, field_name="Значение"):
    """
    Проверяет, что значение — положительное целое число.

    :param value: строка с числом
    :param field_name: название поля для сообщения
    :return: (True, число) или (False, сообщение об ошибке)
    """
    try:
        number = int(value)
        if number <= 0:
            return False, f"{field_name} должно быть больше нуля"
        return True, number
    except (ValueError, TypeError):
        return False, f"{field_name} должно быть целым числом"