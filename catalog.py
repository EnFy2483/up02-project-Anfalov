"""Каталог товаров: карточка товара по макету."""
import tkinter as tk
from typing import Literal

from styles import (
    COLOR_MAIN_BG,
    COLOR_HIGHLIGHT,
    FONT_SIZE_NORMAL,
    FONT_SIZE_HEADER,
    font
)
from resources import get_product_image


# Глобальный список для хранения ссылок на изображения
_image_refs = []

AlignType = Literal["w", "e", "center", "n", "s", "nw", "ne", "sw", "se"]


def create_product_card(parent, product, refresh=None, client=None):
    """
    Создаёт карточку товара по макету.

    :param parent: родительский контейнер
    :param product: объект Product
    :param refresh: callback для обновления каталога после заказа
    :param client: ФИО авторизованного пользователя (для заказа)
    """
    qty = product.quantity
    bg_color = _get_card_color(qty)

    # === ДИАГНОСТИКА (пара 15, задание 5.2) ===
    print(f"[CARD] id={product.id}, name={product.name}, "
          f"qty={qty}, bg={bg_color}, indicator={_indicator(qty)}")

    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    _add_image(card, product, bg_color)
    _add_text_info(card, product, bg_color, qty)

    separator = tk.Frame(parent, height=2, bg="#cccccc")
    separator.pack(fill="x", padx=10)

    # === ПРИВЯЗКА КЛИКА (пара 19) ===
    card.bind("<Button-1>",
              lambda e: _open_view(parent, product, refresh, client))
    for child in card.winfo_children():
        child.bind("<Button-1>",
                   lambda e: _open_view(parent, product, refresh, client))

    return card


def _open_view(parent, product, refresh=None, client=None):
    """Открывает форму просмотра товара."""
    from view_form import ViewForm
    # Окно привязываем к главному окну, а не к фрейму каталога,
    # иначе refresh_catalog уничтожит его вместе с карточками
    ViewForm(parent.winfo_toplevel(), product,
             on_add_to_order=refresh, client=client)


def _get_card_color(qty):
    """Возвращает цвет фона карточки."""
    return COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG


def _add_image(card, product, bg_color):
    """Добавляет изображение товара (или заглушку)."""
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    try:
        photo = get_product_image(None, size=(100, 100))
        if photo:
            img_label = tk.Label(img_frame, image=photo, bg=bg_color)
            img_label.pack()
            _image_refs.append(photo)
        else:
            raise ValueError("Нет изображения")
    except Exception as e:
        print(f"[DEBUG] Ошибка загрузки фото: {e}")
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color,
                 width=10, height=5).pack()


def _add_text_info(card, product, bg_color, qty):
    """Добавляет текстовую информацию о товаре."""
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # --- Обработка крайних случаев ---
    name = product.name if product.name else "[Без названия]"
    production = product.supplier if product.supplier else "[Без производства]"
    category = product.category if product.category else "[Без категории]"
    composition = product.description if product.description else "[Не указан]"
    price = product.price if product.price is not None else 0

    _add_label(text_frame, f"{production} | {name}",
               bg_color, bold=True, size=FONT_SIZE_HEADER)
    _add_label(text_frame, f"Категория: {category}", bg_color)
    _add_label(text_frame, f"Количество: {_indicator(qty)} ({qty})", bg_color)
    _add_label(text_frame, f"Состав: {composition}", bg_color)
    _add_label(text_frame, f"{price} руб.",
               bg_color, bold=True, size=FONT_SIZE_HEADER, align="e")


def _add_label(parent, text, bg_color, bold=False,
               size=FONT_SIZE_NORMAL, align: AlignType = "w"):
    """Добавляет метку с текстом."""
    tk.Label(parent, text=text, font=font(size, bold=bold),
             bg=bg_color, anchor=align).pack(fill="x")


def _indicator(qty):
    """
    Индикатор «много/мало» (порог 5).

    :param qty: количество товара
    :return: «много» или «мало»
    """
    return "много" if qty > 5 else "мало"