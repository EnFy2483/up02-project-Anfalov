<<<<<<< HEAD
=======
<<<<<<< HEAD
from models import Product

p = Product(
    product_id=1,
    name="Ноутбук",
    category="Электроника",
    description='15.6", 16 ГБ ОЗУ',
    price=54990,
    supplier="ООО Техно",
    quantity=3
)

print(p.info())
print(f"Со скидкой 25%: {p.price_with_discount(25):.2f} руб.")
=======
>>>>>>> 403cc53a2244b6cc27b21c6ea83745ec0123f84b
from models import Product

p = Product(
    product_id=1,
    name="Ноутбук",
    category="Электроника",
    description='15.6", 16 ГБ ОЗУ',
    price=54990,
    supplier="ООО Техно",
    quantity=3
)

print(p.info())
print(f"Со скидкой 25%: {p.price_with_discount(25):.2f} руб.")
<<<<<<< HEAD
=======
>>>>>>> 8ca90ff (Пара 3: класс Product и загрузка из БД)
>>>>>>> 403cc53a2244b6cc27b21c6ea83745ec0123f84b
print(f"В наличии: {p.is_available()}")