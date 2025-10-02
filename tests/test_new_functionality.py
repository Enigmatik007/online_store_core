"""Тесты для новой функциональности - обработка исключений и средний ценник."""

import pytest
from src.models import Product, Category, ZeroQuantityError


class TestProductZeroQuantity:
    """Тесты для обработки нулевого количества товара."""

    def test_product_creation_with_zero_quantity_raises_error(self) -> None:
        """Тестирует, что создание товара с нулевым количеством вызывает ValueError."""
        with pytest.raises(
            ZeroQuantityError,
            match="Товар с нулевым количеством не может быть добавлен",
        ):
            Product("Test Product", "Test Description", 100.0, 0)

    def test_product_creation_with_positive_quantity_success(self) -> None:
        """Тестирует успешное создание товара с положительным количеством."""
        product = Product("Test Product", "Test Description", 100.0, 5)
        assert product.quantity == 5
        assert product.name == "Test Product"

    def test_product_creation_with_negative_quantity_raises_error(self) -> None:
        """Проверка создания товара с отрицательным количеством, вызывает ValueError."""
        with pytest.raises(ValueError, match="Количество не может быть отрицательным"):
            Product("Test Product", "Test Description", 100.0, -1)


class TestCategoryAveragePrice:
    """Тесты для метода подсчета среднего ценника категории."""

    def test_average_price_with_products(self) -> None:
        """Тестирует расчет средней цены при наличии товаров."""
        # Создаем товары с разными ценами
        p1 = Product("Product1", "Desc1", 100.0, 5)
        p2 = Product("Product2", "Desc2", 200.0, 3)
        p3 = Product("Product3", "Desc3", 300.0, 2)

        category = Category("Test Category", "Test Description", [p1, p2, p3])

        # Средняя цена: (100 + 200 + 300) / 3 = 200
        assert category.average_price() == 200.0

    def test_average_price_with_single_product(self) -> None:
        """Тестирует расчет средней цены при одном товаре."""
        p1 = Product("Product1", "Desc1", 150.0, 5)
        category = Category("Test Category", "Test Description", [p1])

        assert category.average_price() == 150.0

    def test_average_price_with_empty_category(self) -> None:
        """Тестирует расчет средней цены при пустой категории."""
        category = Category("Test Category", "Test Description", [])

        # Должен вернуть 0 при отсутствии товаров
        assert category.average_price() == 0

    def test_average_price_with_zero_price_products(self) -> None:
        """Тестирует расчет средней цены с товарами нулевой цены."""
        # Создаем товары с нулевой ценой (если это допустимо в бизнес-логике)
        p1 = Product("Product1", "Desc1", 0.0, 5)
        p2 = Product("Product2", "Desc2", 0.0, 3)

        category = Category("Test Category", "Test Description", [p1, p2])

        assert category.average_price() == 0.0

    def test_average_price_after_adding_products(self) -> None:
        """Тестирует пересчет средней цены после добавления товаров."""
        p1 = Product("Product1", "Desc1", 100.0, 5)
        category = Category("Test Category", "Test Description", [p1])

        assert category.average_price() == 100.0

        # Добавляем еще один товар
        p2 = Product("Product2", "Desc2", 300.0, 2)
        category.add_product(p2)

        # Средняя цена теперь: (100 + 300) / 2 = 200
        assert category.average_price() == 200.0


class TestZeroQuantityErrorIntegration:
    """Интеграционные тесты для пользовательского исключения ZeroQuantityError."""

    def test_zero_quantity_error_inheritance(self) -> None:
        """Тестирует, что ZeroQuantityError наследуется от Exception."""
        assert issubclass(ZeroQuantityError, Exception)

    def test_zero_quantity_error_message(self) -> None:
        """Тестирует сообщение об ошибке ZeroQuantityError."""
        error = ZeroQuantityError("Товар с нулевым количеством не может быть добавлен")
        assert str(error) == "Товар с нулевым количеством не может быть добавлен"

    def test_product_creation_zero_quantity_output(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Тестирует вывод сообщений при создании товара с нулевым количеством."""
        try:
            Product("Test", "Test", 100.0, 0)
        except ZeroQuantityError:
            pass

        captured = capsys.readouterr()
        assert "Товар с нулевым количеством не может быть добавлен" in captured.out
        assert "Обработка добавления товара завершена" in captured.out
        assert "Товар успешно добавлен" not in captured.out

    def test_product_creation_positive_quantity_output(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Тестирует вывод сообщений при успешном создании товара."""
        Product("Test", "Test", 100.0, 5)

        captured = capsys.readouterr()
        assert "Товар успешно добавлен" in captured.out
        assert "Обработка добавления товара завершена" in captured.out
        assert "Товар с нулевым количеством не может быть добавлен" not in captured.out


def test_coverage_requirements() -> None:
    """Тест для проверки покрытия функционального кода."""
    # Создаем и тестируем различные сценарии для обеспечения покрытия >75%

    # Тест успешного создания
    p1 = Product("P1", "D1", 100.0, 1)
    p2 = Product("P2", "D2", 200.0, 2)

    # Тест категории с товарами
    cat = Category("Cat", "Desc", [p1, p2])
    assert cat.average_price() == 150.0

    # Тест пустой категории
    empty_cat = Category("Empty", "Desc", [])
    assert empty_cat.average_price() == 0
