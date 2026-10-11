"""ДЗ: индикатор «много/мало» (порог 5)."""
from task_03_catalog import catalog


def indicator(qty):
    """«много», если qty > 5, иначе «мало»."""
    return "много" if qty > 5 else "мало"


# Сначала «много», внутри группы — по убыванию количества
sorted_catalog = sorted(catalog,
                        key=lambda item: (indicator(item["qty"]) != "много",
                                          -item["qty"]))

print("Каталог с индикатором:")
for number, item in enumerate(sorted_catalog, start=1):
    print(f"{number}. {item['name']:<10} — {item['qty']} шт. "
          f"→ {indicator(item['qty'])}")
