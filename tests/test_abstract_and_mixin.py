"""Тесты для абстрактного класса BaseProduct и миксина ReprMixin."""

import pytest
from abc import ABC

from src.models import BaseProduct, Product, Smartphone, LawnGrass, ReprMixin


def test_base_product_is_abstract() -> None:
    """Тестирует, что BaseProduct является абстрактным классом."""
    assert issubclass(BaseProduct, ABC)
    assert (
        len(BaseProduct.__abstractmethods__) > 0
    )  # Убедимся, что есть абстрактные методы


def test_cannot_instantiate_base_product_directly() -> None:
    """Тестирует, что нельзя напрямую создать экземпляр BaseProduct."""
    with pytest.raises(TypeError):
        BaseProduct("Test", "Test", 100.0, 10)  # type: ignore


def test_product_inherits_from_base_product() -> None:
    """Тестирует, что Product наследуется от BaseProduct."""
    assert issubclass(Product, BaseProduct)


def test_smartphone_inherits_from_product() -> None:
    """Тестирует, что Smartphone наследуется от Product."""
    assert issubclass(Smartphone, Product)


def test_lawn_grass_inherits_from_product() -> None:
    """Тестирует, что LawnGrass наследуется от Product."""
    assert issubclass(LawnGrass, Product)


def test_repr_mixin_functionality(capsys: pytest.CaptureFixture[str]) -> None:
    """Тестирует функциональность миксина ReprMixin."""
    Product("Test Product", "Test Description", 100.0, 5)
    captured = capsys.readouterr()
    assert "Создан объект: Product(" in captured.out


def test_repr_mixin_repr_method() -> None:
    """Тестирует метод __repr__ миксина ReprMixin."""
    product = Product("Test", "Desc", 100.0, 5)
    repr_str = repr(product)
    assert "Product(" in repr_str


def test_all_products_have_repr_mixin() -> None:
    """Тестирует, что все классы продуктов имеют миксин ReprMixin."""
    assert ReprMixin in Product.__mro__
    assert ReprMixin in Smartphone.__mro__
    assert ReprMixin in LawnGrass.__mro__


def test_abstract_methods_implementation() -> None:
    """Тестирует, что все абстрактные методы реализованы в Product."""
    product = Product("Test", "Desc", 100.0, 5)

    # Проверяем наличие методов
    assert hasattr(product, '__init__')
    assert hasattr(product, '__str__')
    assert hasattr(product, '__add__')
    assert hasattr(product, 'name')
    assert hasattr(product, 'description')
    assert hasattr(product, 'price')
    assert hasattr(product, 'quantity')

    # Проверяем работоспособность
    assert isinstance(str(product), str)
    assert isinstance(product.name, str)
    assert isinstance(product.description, str)
    assert isinstance(product.price, float)
    assert isinstance(product.quantity, int)


class TestReprMixinStandalone:
    """Тесты для миксина ReprMixin отдельно."""

    def test_repr_mixin_alone(self) -> None:
        """Тестирует миксин ReprMixin на отдельном классе."""

        class TestClass(ReprMixin):
            __slots__ = ('param1', 'param2')

            def __init__(self, param1: str, param2: int) -> None:
                self.param1 = param1
                self.param2 = param2

        obj = TestClass("test", 42)
        repr_str = repr(obj)

        assert "TestClass(" in repr_str
        assert "param1='test'" in repr_str
        assert "param2=42" in repr_str
