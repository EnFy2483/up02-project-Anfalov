"""Главное окно с каталогом."""
import os
import tkinter as tk
from tkinter import ttk

from styles import (
    COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
from config import APP_TITLE
import db_products as db
from catalog import create_product_card
from db_users import get_user_fio
from resources import load_image_proportional, PATH_LOGO, PATH_ICON


_image_refs = []


def set_app_icon(root, icon_path):
    """Устанавливает иконку приложения кроссплатформенно."""
    try:
        if os.name == "nt":
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        else:
            png_path = icon_path.replace(".ico", ".png")
            icon_img = load_image_proportional(png_path, max_size=(32, 32))
            if icon_img:
                root.iconphoto(True, icon_img)
                root._icon_photo = icon_img
    except Exception as e:
        print(f"Не удалось установить иконку: {e}")


class CatalogWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("900x700")
        set_app_icon(self.root, PATH_ICON)
        self.current_user = None
        self.user_label = None
        self.build_ui()
        self.load_products()
        self.require_auth()

    def build_ui(self):
        header = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        logo = load_image_proportional(PATH_LOGO, max_size=(60, 60))
        if logo:
            logo_label = tk.Label(header, image=logo, bg=COLOR_SECONDARY_BG)
            logo_label.pack(side="left", padx=15)
            _image_refs.append(logo)
        else:
            tk.Label(header, text="[ЛОГОТИП]",
                     bg=COLOR_SECONDARY_BG).pack(side="left", padx=15)

        # Правый верхний угол: ФИО пользователя + кнопки по роли.
        # Пакуем до заголовка, чтобы pack оставил место справа.
        self.right_frame = tk.Frame(header, bg=COLOR_SECONDARY_BG)
        self.right_frame.pack(side="right", padx=15)

        self.user_label = tk.Label(self.right_frame, text="Не авторизован",
                                   font=font(FONT_SIZE_NORMAL),
                                   bg=COLOR_SECONDARY_BG)
        self.user_label.pack(side="right", padx=5)

        tk.Label(header, text="КАТАЛОГ ТОВАРОВ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(expand=True)

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

    def load_products(self):
        """Загружает товары с обработкой ошибок."""
        from error_handler import safe_call

        client = get_user_fio(self.current_user) if self.current_user else None

        products = safe_call(db.get_all_products) or []
        for p in products:
            safe_call(create_product_card, self.catalog_frame, p,
                      refresh=self.refresh_catalog, client=client)

    def refresh_catalog(self):
        """Обновляет каталог."""
        for widget in self.catalog_frame.winfo_children():
            widget.destroy()
        self.load_products()

    def require_auth(self):
        """Запрашивает авторизацию."""
        from auth import AuthWindow
        AuthWindow(self.root, self.on_auth_success)

    def on_auth_success(self, user):
        """
        Обработчик входа.

        :param user: кортеж (id, фамилия, имя, отчество, логин, роль)
                     или None — гость
        """
        self.current_user = user

        if user is None:
            self.user_label.config(text="Гость")
            return

        # ФИО в правом верхнем углу
        self.user_label.config(text=f"{get_user_fio(user)} ({user[5]})")
        self.add_role_buttons(user[5])
        # Карточки пересоздаём, чтобы заказы шли на ФИО пользователя
        self.refresh_catalog()

    def add_role_buttons(self, role):
        """
        Добавляет кнопки в зависимости от роли.

        :param role: название роли
        """
        if role in ("Менеджер", "Администратор"):
            tk.Button(self.right_frame, text="Заказы",
                      command=self.open_orders,
                      bg=COLOR_ACCENT, fg="white",
                      font=font(FONT_SIZE_NORMAL),
                      padx=10, pady=5).pack(side="left", padx=5)

        if role == "Администратор":
            tk.Button(self.right_frame, text="Админ-панель",
                      command=self.open_admin,
                      bg=COLOR_ACCENT, fg="white",
                      font=font(FONT_SIZE_NORMAL),
                      padx=10, pady=5).pack(side="left", padx=5)

    def open_orders(self):
        """Открывает окно списка заказов."""
        from orders_window import OrdersWindow
        OrdersWindow(self.root, self.current_user)

    def open_admin(self):
        """Открывает админ-панель."""
        from admin_panel import AdminPanel
        AdminPanel(self.root, self.current_user)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    CatalogWindow().run()