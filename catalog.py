"""Каталог товаров: карточка товара по макету."""
import tkinter as tk

from styles import (
    COLOR_HIGHLIGHT,
    FONT_SIZE_NORMAL,
    FONT_SIZE_HEADER,
    font
)
from resources import get_product_image


# Глобальный список для хранения ссылок на изображения —
# иначе Python удалит их сборщиком мусора
_image_refs = []


def create_product_card(parent, product):
    """
    Создаёт карточку товара по макету.

    :param parent: родительский контейнер (Frame)
    :param product: объект Product из models.py
    :return: Frame — карточка товара
    """
    # --- Определяем фон: подсветка, если количество ≤ 3 ---
    qty = product.quantity
    bg_color = COLOR_HIGHLIGHT if qty <= 3 else "white"

    # --- Карточка — рамка со всех сторон ---
    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    # ============ ИЗОБРАЖЕНИЕ (слева) ============
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    # get_product_image сам подставит заглушку, если картинки нет
    photo = get_product_image(None, size=(100, 100))
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.pack()
        _image_refs.append(photo)   # сохраняем ссылку!
    else:
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color,
                 width=10, height=5).pack()

    # ============ ТЕКСТОВАЯ ЧАСТЬ (справа) ============
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Производство | Наименование
    title = f"{product.supplier} | {product.name}"
    tk.Label(text_frame, text=title,
             font=font(FONT_SIZE_HEADER, bold=True),
             bg=bg_color, anchor="w").pack(fill="x")

    # Категория
    tk.Label(text_frame, text=f"Категория: {product.category}",
             font=font(FONT_SIZE_NORMAL),
             bg=bg_color, anchor="w").pack(fill="x")

    # Количество (индикатор «много» / «мало»)
    indicator = "много" if qty > 5 else "мало"
    tk.Label(text_frame, text=f"Количество: {indicator} ({qty})",
             font=font(FONT_SIZE_NORMAL),
             bg=bg_color, anchor="w").pack(fill="x")

    # Состав (описание)
    tk.Label(text_frame, text=f"Состав: {product.description}",
             font=font(FONT_SIZE_NORMAL),
             bg=bg_color, anchor="w").pack(fill="x")

    # Цена (справа)
    tk.Label(text_frame, text=f"{product.price} руб.",
             font=font(FONT_SIZE_HEADER, bold=True),
             bg=bg_color, anchor="e").pack(fill="x")

    # === РАЗДЕЛИТЕЛЬ между карточками (ДЗ 10-й пары) ===
    separator = tk.Frame(parent, height=2, bg="#cccccc")
    separator.pack(fill="x", padx=10)

    return card