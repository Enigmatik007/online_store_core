"""Тесты дополнительных функций для моделей Product и Category."""

import pytest
from src.models import Product, Category


def test_product_new_product_basic_and_duplicate() -> None:
    """Тестирует создание продукта и обработку дубликатов."""
    # Базовый случай: создание нового продукта
    data = {"name": "SSD 1TB", "description": "Fast SSD", "price": 120.0, "quantity": 4}
    p = Product.new_product(data)
    assert isinstance(p, Product)
    assert p.name == "SSD 1TB"
    assert p.description == "Fast SSD"
    assert p.price == 120.0
    assert p.quantity == 4

    # Дополнительное задание: дубликат по имени в existing_products
    existing = [
        Product(name="SSD 1TB", description="Fast SSD", price=110.0, quantity=2)
    ]
    p2 = Product.new_product(data, existing_products=existing)
    assert p2 is existing[0]
    assert existing[0].quantity == 6  # 2 + 4
    assert existing[0].price == 120.0  # более высокая цена (120 > 110)


def test_product_price_setter_validation_and_interactive(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Тестирует валидацию и интерактивное изменение цены продукта.

    Args:
        monkeypatch: Фикстура для мокирования ввода
        capsys: Фикстура для перехвата вывода
    """
    prod = Product(name="Keyboard", description="Mechanical", price=100.0, quantity=5)

    # Попытка установить недопустимую цену
    prod.price = 0
    assert prod.price == 100.0
    out = capsys.readouterr().out
    assert "Цена не должна быть нулевая или отрицательная" in out

    # Снижение цены с подтверждением "y"
    monkeypatch.setattr("builtins.input", lambda prompt=None: "y")
    prod.price = 90.0
    assert prod.price == 90.0

    # Снижение цены с подтверждением отказа "n"
    monkeypatch.setattr("builtins.input", lambda prompt=None: "n")
    prod.price = 80.0
    # Цена не изменилась после отказа
    assert prod.price == 90.0


def test_category_counters_increment_and_product_list() -> None:
    """Тестирует счетчики категорий и товаров."""
    # Проверяем счетчики при создании новой Category
    before_categories = Category.total_categories
    before_products = Category.total_products

    new_cat = Category(name="New Category", description="Desc", products=[])
    assert isinstance(new_cat, Category)
    assert new_cat.product_list == []
    # Категория добавлена: счетчик категорий увеличился на 1
    assert Category.total_categories == before_categories + 1
    # Количество товаров не изменилось (пустой список)
    assert Category.total_products == before_products
