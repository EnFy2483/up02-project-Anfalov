"""Авторизация пользователей."""
import tkinter as tk
from tkinter import messagebox

from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_SMALL, FONT_SIZE_TITLE, font
)
from db_users import get_user_by_login


class AuthWindow:
    """Окно авторизации (вход только по логину, без пароля — по КИМ)."""

    def __init__(self, root, on_success):
        """
        Инициализация окна.

        :param root: главное окно
        :param on_success: callback при успешной авторизации
        """
        self.root = root
        self.on_success = on_success
        self.current_user = None

        self.window = tk.Toplevel(root)
        self.window.title("Авторизация")
        self.window.geometry("400x320")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.window.transient(root)
        # Закрытие окна крестиком = вход гостем (неавторизованный)
        self.window.protocol("WM_DELETE_WINDOW", self.login_as_guest)

        self.build_ui()

        try:
            self.window.grab_set()
        except tk.TclError:
            pass

    def build_ui(self):
        """Строит интерфейс окна."""
        # Шапка
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="ВХОД В СИСТЕМУ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        # Логин
        form = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        form.pack(pady=20)

        tk.Label(form, text="Логин:", font=font(FONT_SIZE_NORMAL),
                 bg=COLOR_MAIN_BG).pack(anchor="w")

        self.login_var = tk.StringVar()
        login_entry = tk.Entry(form, textvariable=self.login_var, width=30,
                               font=font(FONT_SIZE_NORMAL))
        login_entry.pack(pady=5)
        login_entry.focus_set()
        login_entry.bind("<Return>", lambda e: self.login())

        # Кнопки
        tk.Button(form, text="Войти", command=self.login,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=20, pady=5).pack(pady=10)

        tk.Button(form, text="Войти как гость", command=self.login_as_guest,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_SMALL),
                  padx=10, pady=2).pack()

        # Подсказка
        tk.Label(form, text="Пример: client1, manager1, admin1",
                 font=font(FONT_SIZE_SMALL),
                 fg="gray", bg=COLOR_MAIN_BG).pack(pady=5)

    def login(self):
        """Обработчик входа."""
        login = self.login_var.get().strip()

        if not login:
            messagebox.showwarning("Ошибка", "Введите логин",
                                   parent=self.window)
            return

        try:
            user = get_user_by_login(login)
        except Exception as e:
            messagebox.showerror("Ошибка БД", str(e), parent=self.window)
            return

        if not user:
            messagebox.showerror("Ошибка", "Пользователь не найден",
                                 parent=self.window)
            return

        self.current_user = user
        messagebox.showinfo("Успех", f"Добро пожаловать, {user[2]}!",
                            parent=self.window)
        self.window.destroy()
        self.on_success(user)

    def login_as_guest(self):
        """Вход без авторизации — только просмотр каталога."""
        self.window.destroy()
        self.on_success(None)
