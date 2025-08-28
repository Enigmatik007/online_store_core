from decimal import Decimal
from pathlib import Path
from typing import Type
import json
import pytest

from src.models import Category, Product, Smartphone, LawnGrass


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

    def test_product_str(self) -> None:
        """Тестирует строковое представление продукта."""
        product = Product(name="Test", description="Test", price=100.0, quantity=5)
        assert str(product) == "Test, 100 руб. Остаток: 5 шт."

    def test_product_addition(self) -> None:
        """Тестирует сложение продуктов."""
        p1 = Product(name="A", description="", price=100, quantity=2)
        p2 = Product(name="B", description="", price=200, quantity=3)
        assert p1 + p2 == 100 * 2 + 200 * 3

    def test_product_addition_type_error(self) -> None:
        """Тестирует TypeError при сложении с не-Product."""
        p = Product(name="A", description="", price=100, quantity=1)
        with pytest.raises(TypeError):
            p + "invalid"  # type: ignore[operator]


class TestSmartphone:
    """Тесты для класса Smartphone."""

    def test_smartphone_creation(self) -> None:
        """Тестирует создание смартфона."""
        phone = Smartphone(
            name="iPhone",
            description="Cool phone",
            price=1000,
            quantity=5,
            efficiency=2.5,
            model="15 Pro",
            memory=256,
            color="Black",
        )
        assert phone.name == "iPhone"
        assert phone.price == 1000
        assert phone.memory == 256
        assert phone.color == "Black"

    def test_smartphone_str(self) -> None:
        """Тестирует строковое представление смартфона."""
        phone = Smartphone(
            name="Galaxy",
            description="",
            price=800,
            quantity=3,
            efficiency=2.0,
            model="S23",
            memory=128,
            color="White",
        )
        assert str(phone) == "Galaxy, 800 руб. Остаток: 3 шт."

    def test_smartphone_addition(self) -> None:
        """Тестирует сложение смартфонов."""
        phone1 = Smartphone(
            name="Phone1",
            description="",
            price=1000,
            quantity=2,
            efficiency=2.5,
            model="M1",
            memory=128,
            color="Black",
        )
        phone2 = Smartphone(
            name="Phone2",
            description="",
            price=2000,
            quantity=3,
            efficiency=3.0,
            model="M2",
            memory=256,
            color="White",
        )
        assert phone1 + phone2 == 1000 * 2 + 2000 * 3

    def test_smartphone_addition_error(self) -> None:
        """Тестирует ошибку при сложении с не-Smartphone."""
        phone = Smartphone(
            name="Phone",
            description="",
            price=1000,
            quantity=1,
            efficiency=2.5,
            model="M1",
            memory=128,
            color="Black",
        )
        grass = LawnGrass(
            name="Grass",
            description="",
            price=500,
            quantity=1,
            country="Russia",
            germination_period=30,
            color="Green",
        )
        with pytest.raises(TypeError):
            phone + grass


class TestLawnGrass:
    """Тесты для класса LawnGrass."""

    def test_lawn_grass_creation(self) -> None:
        """Тестирует создание газонной травы."""
        grass = LawnGrass(
            name="Grass",
            description="Green grass",
            price=500,
            quantity=10,
            country="Russia",
            germination_period=30,
            color="Green",
        )
        assert grass.name == "Grass"
        assert grass.price == 500
        assert grass.country == "Russia"
        assert grass.germination_period == 30

    def test_lawn_grass_str(self) -> None:
        """Тестирует строковое представление газонной травы."""
        grass = LawnGrass(
            name="Premium",
            description="",
            price=700,
            quantity=5,
            country="USA",
            germination_period=20,
            color="Blue",
        )
        assert str(grass) == "Premium, 700 руб. Остаток: 5 шт."

    def test_lawn_grass_addition(self) -> None:
        """Тестирует сложение газонных трав."""
        grass1 = LawnGrass(
            name="Grass1",
            description="",
            price=500,
            quantity=2,
            country="RU",
            germination_period=30,
            color="Green",
        )
        grass2 = LawnGrass(
            name="Grass2",
            description="",
            price=300,
            quantity=3,
            country="US",
            germination_period=20,
            color="Blue",
        )
        assert grass1 + grass2 == 500 * 2 + 300 * 3

    def test_lawn_grass_addition_error(self) -> None:
        """Тестирует ошибку при сложении с не-LawnGrass."""
        grass = LawnGrass(
            name="Grass",
            description="",
            price=500,
            quantity=1,
            country="RU",
            germination_period=30,
            color="Green",
        )
        phone = Smartphone(
            name="Phone",
            description="",
            price=1000,
            quantity=1,
            efficiency=2.5,
            model="M1",
            memory=128,
            color="Black",
        )
        with pytest.raises(TypeError):
            grass + phone


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

    def test_category_str(self, sample_category: Category) -> None:
        """Тестирует строковое представление категории."""
        assert str(sample_category) == "Test Category, количество продуктов: 10 шт."

    def test_category_iterator(self, sample_category: Category) -> None:
        """Тестирует итерацию по категории."""
        products = list(sample_category)
        assert len(products) == 1
        assert products[0].name == "Test Product"

    def test_add_smartphone_to_category(self) -> None:
        """Тестирует добавление смартфона в категорию."""
        category = Category("Electronics", "", [])
        phone = Smartphone(
            name="Phone",
            description="",
            price=1000,
            quantity=1,
            efficiency=2.5,
            model="M1",
            memory=128,
            color="Black",
        )
        category.add_product(phone)
        assert phone in category.product_list

    def test_add_lawn_grass_to_category(self) -> None:
        """Тестирует добавление газонной травы в категорию."""
        category = Category("Garden", "", [])
        grass = LawnGrass(
            name="Grass",
            description="",
            price=500,
            quantity=1,
            country="RU",
            germination_period=30,
            color="Green",
        )
        category.add_product(grass)
        assert grass in category.product_list


@pytest.fixture
def sample_product() -> Product:
    """Создает тестовый товар для использования в тестах."""
    return Product(
        name="Test Product", description="Test Description", price=100.0, quantity=10
    )


@pytest.fixture
def sample_category(sample_product: Product) -> Category:
    """Создает тестовую категорию с одним товаром."""
    return Category(
        name="Test Category", description="Test Description", products=[sample_product]
    )


@pytest.fixture
def json_data_file(tmp_path: Path) -> Path:
    """Создает временный JSON-файл с тестовыми данными."""
    data = {
        "name": "Test Category",
        "description": "Test Description",
        "products": [
            {
                "name": "Test Product",
                "description": "Test Description",
                "price": 100.0,
                "quantity": 10,
            }
        ],
    }
    file_path = tmp_path / "test_data.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return file_path
