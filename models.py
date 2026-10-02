"""Модели данных для проекта УП.02."""
from datetime import datetime
from discount import calculate_price_with_discount


class Product:
    """Класс Товар."""

    def __init__(self, product_id, name,    
                 category, description,
                 price, supplier, quantity):
        self.id = product_id         
        self.name = name
        self.category = category
        self.description = description
        self.price = price
        self.supplier = supplier
        self.quantity = quantity

    def total(self):    # ← 4 пробела
        return self.price * self.quantity       

    def price_with_discount_auto(self, date=None):
        if date is None:
            date = datetime.now()
        return calculate_price_with_discount(self, date)

    def indicator(self):
        return "много" if self.quantity > 5 else "мало"

    def is_available(self):
        return self.quantity > 0

    def info(self):
        return (f"{self.name} ({self.category}): "
                f"{self.price} руб. × {self.quantity} = "
                f"{self.total()} руб. ({self.indicator()})")


class Order:
    """Класс Заказ."""

    def __init__(self, order_id, date, client, product, quantity):
        self.id = order_id
        self.date = date
        self.client = client
        self.product = product
        self.quantity = quantity

    def total(self):
        return self.product.price * self.quantity

    def info(self):
        return (f"Заказ №{self.id} от {self.date}: "
                f"{self.client} – {self.product.name} × {self.quantity}")