"""Модели данных для проекта УП.02."""


class Product:
    """Класс Товар."""

    def __init__(self, product_id, name, category, description,
                 price, supplier, quantity):
        """
        Инициализация товара.

        :param product_id: идентификатор
        :param name: название
        :param category: категория
        :param description: описание
        :param price: цена
        :param supplier: поставщик
        :param quantity: количество
        """
        self.id = product_id
        self.name = name
        self.category = category
        self.description = description
        self.price = price
        self.supplier = supplier
        self.quantity = quantity

    def total(self):
        """Общая стоимость (цена × количество)."""
        return self.price * self.quantity

    def price_with_discount(self, discount):
        """Цена со скидкой (discount — процент)."""
        return self.price * (1 - discount / 100)

    def indicator(self):
        """Индикатор «много» / «мало» (порог 5)."""
        return "много" if self.quantity > 5 else "мало"

    def is_available(self):
        """True, если товар есть на складе."""
        return self.quantity > 0

    def info(self):
        """Строка с информацией о товаре."""
        return (f"{self.name} ({self.category}): "
                f"{self.price} руб. × {self.quantity} = "
                f"{self.total()} руб. ({self.indicator()})")