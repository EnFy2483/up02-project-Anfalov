"""Главное окно приложения с каталогом."""
import os
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from config import APP_TITLE, FONT_FAMILY, COLOR_HEADER
import db_products as db
from catalog import create_product_card


# Глобальный список для ссылок на изображения
_image_refs = []


class CatalogWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("900x700")
        self.build_ui()
        self.load_products()

    def build_ui(self):
        # Шапка
        header = tk.Frame(self.root, bg=COLOR_HEADER)
        header.pack(fill="x")

        # Логотип
        logo_path = "resources/logo.png"
        if os.path.exists(logo_path):
            try:
                logo = Image.open(logo_path).resize((50, 50))
                logo_photo = ImageTk.PhotoImage(logo)
                logo_label = tk.Label(header, image=logo_photo, bg=COLOR_HEADER)
                logo_label.pack(side="left", padx=10, pady=10)
                _image_refs.append(logo_photo)
            except Exception as e:
                print(f"Ошибка загрузки логотипа: {e}")

        tk.Label(header, text="КАТАЛОГ ТОВАРОВ",
                 font=(FONT_FAMILY, 16, "bold"),
                 bg=COLOR_HEADER).pack(side="left", pady=15)

        # Область с прокруткой
        body = tk.Frame(self.root, bg="white")
        body.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(body, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(body, orient="vertical",
                                  command=self.canvas.yview)

        self.catalog_frame = tk.Frame(self.canvas, bg="white")
        self.catalog_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.catalog_frame,
                                  anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )

    def load_products(self):
        for widget in self.catalog_frame.winfo_children():
            widget.destroy()

        products = db.get_all_products()
        for p in products:
            create_product_card(self.catalog_frame, p)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    CatalogWindow().run()