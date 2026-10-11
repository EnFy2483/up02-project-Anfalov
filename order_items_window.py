"""Окно состава заказа."""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT, COLOR_HIGHLIGHT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
import order_manager as om


class OrderItemsWindow:
    """Окно состава заказа (Администратор может редактировать)."""

    def __init__(self, parent, order_id, current_user=None, on_change=None):
        """
        Инициализация окна.

        :param parent: родительское окно
        :param order_id: id заказа
        :param current_user: текущий пользователь
        :param on_change: callback — обновить список заказов после правки
        """
        self.order_id = order_id
        self.current_user = current_user
        self.on_change = on_change

        self.window = tk.Toplevel(parent)
        self.window.title(f"Состав заказа №{order_id}")
        self.window.geometry("900x600")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()
        self.load_order_info()
        self.load_items()

    def is_admin(self):
        """Проверяет, является ли пользователь Администратором."""
        return bool(self.current_user and
                    self.current_user[5] == "Администратор")

    def build_ui(self):
        """Строит интерфейс окна."""
        # Шапка
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text=f"СОСТАВ ЗАКАЗА №{self.order_id}",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        # Информация о заказе
        info_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        info_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(info_frame, text="Дата заказа:",
                 font=font(FONT_SIZE_NORMAL, bold=True),
                 bg=COLOR_MAIN_BG).pack(side="left", padx=5)

        self.date_var = tk.StringVar()
        self.date_entry = tk.Entry(info_frame, textvariable=self.date_var,
                                   width=15, font=font(FONT_SIZE_NORMAL),
                                   state="readonly")
        self.date_entry.pack(side="left", padx=5)

        if self.is_admin():
            self.date_entry.config(state="normal")
            tk.Button(info_frame, text="Сохранить дату",
                      command=self.save_date,
                      bg=COLOR_ACCENT, fg="white",
                      font=font(FONT_SIZE_NORMAL),
                      padx=10, pady=3).pack(side="left", padx=10)

        tk.Label(info_frame, text="Клиент:",
                 font=font(FONT_SIZE_NORMAL, bold=True),
                 bg=COLOR_MAIN_BG).pack(side="left", padx=20)

        self.client_label = tk.Label(info_frame, text="",
                                     font=font(FONT_SIZE_NORMAL),
                                     bg=COLOR_MAIN_BG)
        self.client_label.pack(side="left")

        # Кнопки
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(side="bottom", fill="x", pady=10)

        if self.is_admin():
            tk.Button(btn_frame, text="Удалить позицию",
                      command=self.delete_item,
                      bg=COLOR_HIGHLIGHT, fg="white",
                      font=font(FONT_SIZE_NORMAL),
                      padx=15, pady=5).pack(side="left", padx=20)

        tk.Button(btn_frame, text="Обновить",
                  command=self.refresh_all,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Назад",
                  command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="right", padx=20)

        # Итоговая сумма
        self.total_label = tk.Label(self.window, text="",
                                    font=font(FONT_SIZE_NORMAL, bold=True),
                                    fg=COLOR_ACCENT,
                                    bg=COLOR_MAIN_BG)
        self.total_label.pack(side="bottom", pady=5)

        # Таблица позиций
        columns = ("id", "name", "production", "size",
                   "quantity", "price", "total")
        self.tree = ttk.Treeview(self.window, columns=columns,
                                 show="headings", height=12)

        self.tree.heading("id", text="№")
        self.tree.heading("name", text="Товар")
        self.tree.heading("production", text="Производство")
        self.tree.heading("size", text="Размер")
        self.tree.heading("quantity", text="Кол-во")
        self.tree.heading("price", text="Цена")
        self.tree.heading("total", text="Сумма")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("name", width=180, anchor="w")
        self.tree.column("production", width=110, anchor="w")
        self.tree.column("size", width=60, anchor="center")
        self.tree.column("quantity", width=60, anchor="center")
        self.tree.column("price", width=90, anchor="e")
        self.tree.column("total", width=90, anchor="e")

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    def load_order_info(self):
        """Загружает дату и клиента заказа."""
        order = om.get_order_by_id(self.order_id)
        if order:
            state = self.date_entry.cget("state")
            self.date_entry.config(state="normal")
            self.date_var.set(order[1])
            self.date_entry.config(state=state)
            self.client_label.config(text=order[2])

    def load_items(self):
        """Загружает позиции заказа."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            items = om.get_order_items(self.order_id)
            if not items:
                self.total_label.config(text="ИТОГО: 0.00 руб. (заказ пуст)")
                return

            for item in items:
                # item = (id, название, производство, размер, количество, цена)
                item_id = item[0]
                name = item[1]
                production = item[2]
                size = item[3]
                quantity = item[4]
                price = item[5]
                item_total = quantity * price

                self.tree.insert("", tk.END,
                                 values=(item_id, name, production or "—",
                                         size or "—", quantity,
                                         f"{price:.2f}",
                                         f"{item_total:.2f}"))

            total = om.get_order_total(self.order_id)
            self.total_label.config(text=f"ИТОГО: {total:.2f} руб.")

        except Exception as e:
            messagebox.showerror("Ошибка",
                                 f"Не удалось загрузить состав:\n{e}",
                                 parent=self.window)

    def save_date(self):
        """Сохраняет изменённую дату."""
        new_date = self.date_var.get().strip()

        try:
            datetime.strptime(new_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка",
                                 "Неверный формат даты. "
                                 "Используйте ГГГГ-ММ-ДД",
                                 parent=self.window)
            return

        if om.update_order_date(self.order_id, new_date):
            messagebox.showinfo("Успех", "Дата обновлена",
                                parent=self.window)
            self.refresh_all()
        else:
            messagebox.showerror("Ошибка", "Не удалось обновить дату",
                                 parent=self.window)

    def delete_item(self):
        """Удаляет выбранную позицию."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите позицию",
                                   parent=self.window)
            return

        item = self.tree.item(selected[0])
        item_id = item["values"][0]

        if not messagebox.askyesno("Подтверждение",
                                   f"Удалить позицию №{item_id}?",
                                   parent=self.window):
            return

        if om.delete_order_item(item_id):
            messagebox.showinfo("Успех",
                                "Позиция удалена, товар возвращён на склад",
                                parent=self.window)
            self.refresh_all()
        else:
            messagebox.showerror("Ошибка", "Не удалось удалить позицию",
                                 parent=self.window)

    def refresh_all(self):
        """Обновляет окно и список заказов после изменений."""
        self.load_order_info()
        self.load_items()
        if self.on_change:
            self.on_change()
