"""Каталог товаров: карточка товара по макету."""
import os
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from config import COLOR_HIGHLIGHT, FONT_FAMILY


# Глобальный список для хранения ссылок на изображения —
# иначе Python удалит их сборщиком мусора
_image_refs = []


def create_product_card(parent, product):
    """Создаёт карточку товара по макету."""
    qty = product.quantity
    bg_color = COLOR_HIGHLIGHT if qty <= 3 else "white"

    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    # === Изображение ===
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    image_path = "resources/picture.png"
    if os.path.exists(image_path):
        try:
            img = Image.open(image_path).resize((100, 100))
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(img_frame, image=photo, bg=bg_color)
            img_label.pack()
            _image_refs.append(photo)   # ← сохраняем ссылку
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            tk.Label(img_frame, text="[ФОТО]", bg=bg_color,
                     width=10, height=5).pack()
    else:
        tk.Label(img_frame, text="[ФОТО]", bg=bg_color,
                 width=10, height=5).pack()

    # === Текст ===
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    tk.Label(text_frame, text=f"{product.supplier} | {product.name}",
             font=(FONT_FAMILY, 14, "bold"),
             bg=bg_color, anchor="w").pack(fill="x")

    tk.Label(text_frame, text=f"Категория: {product.category}",
             font=(FONT_FAMILY, 11),
             bg=bg_color, anchor="w").pack(fill="x")

    indicator = "много" if qty > 5 else "мало"
    tk.Label(text_frame, text=f"Количество: {indicator} ({qty})",
             font=(FONT_FAMILY, 11),
             bg=bg_color, anchor="w").pack(fill="x")

    tk.Label(text_frame, text=f"Состав: {product.description}",
             font=(FONT_FAMILY, 11),
             bg=bg_color, anchor="w").pack(fill="x")

    tk.Label(text_frame, text=f"{product.price} руб.",
             font=(FONT_FAMILY, 14, "bold"),
             bg=bg_color, anchor="e").pack(fill="x")

    return card