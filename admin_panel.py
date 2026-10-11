"""Админ-панель: список пользователей системы."""
import tkinter as tk
from tkinter import ttk, messagebox

from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
from db_users import get_all_users


class AdminPanel:
    """Окно Администратора."""

    def __init__(self, parent, current_user=None):
        """
        Инициализация окна.

        :param parent: родительское окно
        :param current_user: текущий пользователь
        """
        self.current_user = current_user

        self.window = tk.Toplevel(parent)
        self.window.title("Админ-панель")
        self.window.geometry("700x400")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()
        self.load_users()

    def build_ui(self):
        """Строит интерфейс окна."""
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="ПОЛЬЗОВАТЕЛИ СИСТЕМЫ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(side="bottom", fill="x", pady=10)

        tk.Button(btn_frame, text="Назад",
                  command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="right", padx=20)

        columns = ("id", "fio", "login", "role")
        self.tree = ttk.Treeview(self.window, columns=columns,
                                 show="headings", height=10)

        self.tree.heading("id", text="№")
        self.tree.heading("fio", text="ФИО")
        self.tree.heading("login", text="Логин")
        self.tree.heading("role", text="Роль")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("fio", width=300, anchor="w")
        self.tree.column("login", width=120, anchor="w")
        self.tree.column("role", width=140, anchor="w")

        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

    def load_users(self):
        """Загружает пользователей из БД."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            for user in get_all_users():
                self.tree.insert("", tk.END, values=user)
        except Exception as e:
            messagebox.showerror("Ошибка",
                                 f"Не удалось загрузить пользователей:\n{e}")
