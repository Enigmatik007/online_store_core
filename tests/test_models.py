from decimal import Decimal
from pathlib import Path
from typing import Type

import pytest

from src.models import Category, Product


class TestProduct:
    """Тесты для класса Product."""

    @pytest.mark.parametrize(
        "price,quantity", [(100.0, 10), (Decimal("99.99"), 5), (1, 1)]
    )
    def test_product_creation(self, price: float, quantity: int) -> None:
        """Тестирует создание продукта с разными параметрами."""
        product = Product(
            name="Test", description="Test", price=float(price), quantity=quantity
        )
        assert product.price == float(price)
        assert product.quantity == quantity

    @pytest.mark.parametrize(
        "price,quantity,expected",
        [
            (-100, 10, ValueError),
            (0, 5, ValueError),
            (100, -1, ValueError),
        ],
    )
    def test_product_validation(
        self, price: float, quantity: int, expected: Type[Exception]
    ) -> None:
        """Тестирует валидацию данных продукта."""
        with pytest.raises(expected):
            Product(name="Test", description="Test", price=price, quantity=quantity)

    def test_price_setter_validation(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тестирует валидацию при установке цены."""
        product = Product(name="Test", description="Test", price=100.0, quantity=10)

        # Попытка установить недопустимую цену
        product.price = -50
        assert product.price == 100.0  # Цена не изменилась
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out


class TestCategory:
    """Тесты для класса Category."""

    def test_category_creation(self, sample_category: Category) -> None:
        """Тестирует создание категории."""
        assert sample_category.name == "Test Category"
        assert "Test Product" in sample_category.products

    def test_add_product(
        self, sample_category: Category, sample_product: Product
    ) -> None:
        """Тестирует добавление товара в категорию."""
        initial_count = Category.total_products
        sample_category.add_product(sample_product)
        assert Category.total_products == initial_count + 1

    def test_add_product_typeerror(self, sample_category: Category) -> None:
        """Тестирует добавление в категорию не Product вызывает TypeError."""
        with pytest.raises(TypeError):
            sample_category.add_product("не продукт")  # type: ignore[arg-type]

    def test_from_json(self, json_data_file: Path) -> None:
        """Тестирует создание категории из JSON."""
        category = Category.from_json(json_data_file)
        assert category.name == "Test Category"
        assert "Test Product" in category.products
