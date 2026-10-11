"""Форма просмотра товара."""
import tkinter as tk
from tkinter import ttk, messagebox

from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, FONT_SIZE_TITLE, font
)
from resources import get_product_image
from db_products import get_product_sizes
from error_handler import validate_positive_int
from order_manager import create_order, get_product_quantity

CLIENT_STUB = "Иванов Иван Иванович"


class ViewForm:
    """
    Форма просмотра выбранного товара.
    Открывается при клике на карточку в каталоге.
    """

    def __init__(self, parent, product, on_add_to_order=None, client=None):
        """
        Инициализация формы.

        :param parent: родительское окно
        :param product: объект Product из БД
        :param on_add_to_order: callback для добавления в заказ
        :param client: ФИО клиента (если не вошёл — заглушка)
        """
        self.product = product
        self.on_add_to_order = on_add_to_order
        self.client = client or CLIENT_STUB

        self.window = tk.Toplevel(parent)
        self.window.title(f"Просмотр — {product.name}")
        self.window.geometry("700x600")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.build_ui()

    def build_ui(self):
        """Строит интерфейс формы."""
        # === Шапка ===
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="КАРТОЧКА ТОВАРА",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        # === Основная область ===
        main = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Изображение
        img_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        img_frame.pack(side="left", padx=10)

        photo = get_product_image(None, size=(200, 200))
        if photo:
            img_label = tk.Label(img_frame, image=photo, bg=COLOR_MAIN_BG)
            img_label.image = photo
            img_label.pack()
        else:
            tk.Label(img_frame, text="[НЕТ ФОТО]", bg=COLOR_MAIN_BG,
                     width=15, height=10).pack()

        # === Информация ===
        info_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        info_frame.pack(side="left", fill="both", expand=True, padx=20)

        self._add_field(info_frame, "Производство", self.product.supplier)
        self._add_field(info_frame, "Наименование", self.product.name)
        self._add_field(info_frame, "Категория", self.product.category)
        self._add_field(info_frame, "Состав", self.product.description)
        self._add_field(info_frame, "Цена", f"{self.product.price} руб.")
        self._add_field(info_frame, "Количество", self.product.quantity)

        # === Поле ввода количества ===
        qty_frame = tk.Frame(info_frame, bg=COLOR_MAIN_BG)
        qty_frame.pack(fill="x", pady=10)

        tk.Label(qty_frame, text="Кол-во в заказ:",
                 font=font(FONT_SIZE_NORMAL, bold=True),
                 bg=COLOR_MAIN_BG, width=15, anchor="w").pack(side="left")

        self.qty_var = tk.StringVar(value="1")
        tk.Entry(qty_frame, textvariable=self.qty_var, width=5,
                 font=font(FONT_SIZE_NORMAL)).pack(side="left")

        # === Выбор размера ===
        size_frame = tk.Frame(info_frame, bg=COLOR_MAIN_BG)
        size_frame.pack(fill="x", pady=5)

        tk.Label(size_frame, text="Размер:",
                 font=font(FONT_SIZE_NORMAL, bold=True),
                 bg=COLOR_MAIN_BG, width=15, anchor="w").pack(side="left")

        sizes = get_product_sizes(self.product.id)
        if not sizes:
            sizes = ["—"]

        self.size_var = tk.StringVar(value=sizes[0])
        ttk.Combobox(size_frame, textvariable=self.size_var,
                     values=sizes, state="readonly", width=5,
                     font=font(FONT_SIZE_NORMAL)).pack(side="left")

        # === Кнопки ===
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Добавить в заказ",
                  command=self.add_to_order,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="left", padx=20)

        tk.Button(btn_frame, text="Назад",
                  command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="right", padx=20)

    def _add_field(self, parent, label, value):
        """Добавляет поле в форму."""
        row = tk.Frame(parent, bg=COLOR_MAIN_BG)
        row.pack(fill="x", pady=3)

        tk.Label(row, text=f"{label}:",
                 font=font(FONT_SIZE_NORMAL, bold=True),
                 bg=COLOR_MAIN_BG, width=15, anchor="w").pack(side="left")

        tk.Label(row, text=str(value) if value else "[Не указано]",
                 font=font(FONT_SIZE_NORMAL),
                 bg=COLOR_MAIN_BG, anchor="w").pack(side="left")

    def add_to_order(self):
        """Обработчик кнопки «Добавить в заказ»."""
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return

        ok, result = validate_positive_int(self.qty_var.get(), "Количество")
        if not ok:
            messagebox.showwarning("Ошибка ввода", result)
            return
        qty = result

        try:
            product_id = self.product.id
            current_qty = get_product_quantity(product_id)

            if current_qty < 1:
                messagebox.showwarning("Товар закончился",
                                       f"Товара «{self.product.name}» "
                                       f"больше нет")
                return

            if qty > current_qty:
                messagebox.showwarning("Ошибка ввода",
                                       f"Введите число от 1 до {current_qty}"
                                       f"\n(доступно только {current_qty} шт.)")
                return

            size = self.size_var.get()
            if size == "—":
                size = None

            items = [(product_id, size, qty, self.product.price)]
            # Заказ, состав и остатки — в одной транзакции (create_order)
            order_id = create_order(self.client, items)
            if order_id is None:
                messagebox.showerror("Ошибка заказа",
                                     "Недостаточно товара на складе.\n"
                                     "Заказ не создан, остатки не изменены")
                return

            new_qty = get_product_quantity(product_id)

            messagebox.showinfo("Заказ оформлен",
                                f"Заказ №{order_id} оформлен: {qty} шт., "
                                f"размер {self.size_var.get()}.\n"
                                f"Осталось на складе: {new_qty} шт.")

            if new_qty <= 3:
                messagebox.showwarning("Внимание",
                                       f"Товар «{self.product.name}» "
                                       f"заканчивается! "
                                       f"Осталось {new_qty} шт.")

            if self.on_add_to_order:
                self.on_add_to_order()
            self.window.destroy()

        except Exception as e:
            messagebox.showerror("Ошибка заказа",
                                 f"Не удалось оформить заказ:\n{e}")
