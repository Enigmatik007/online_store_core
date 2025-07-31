import json
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Product:
    """Класс для представления товара в магазине.

    Attributes:
        name: Название товара
        description: Описание товара
        price: Цена товара
        quantity: Количество в наличии
    """

    name: str
    description: str
    price: float
    quantity: int

    def __post_init__(self) -> None:
        """Проводит валидацию данных при инициализации объекта.

        Raises:
            ValueError: Если цена или количество недопустимы
        """
        if self.price <= 0:
            raise ValueError("Цена должна быть положительной")
        if self.quantity < 0:
            raise ValueError("Количество не может быть отрицательным")


class Category:
    """Класс для представления категории товаров.

    Attributes:
        name: Название категории
        description: Описание категории
        total_categories: Счетчик всех категорий
        total_products: Счетчик всех товаров
    """

    total_categories: int = 0
    total_products: int = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        """Инициализирует категорию с товарами."""
        self.name = name
        self.description = description
        self.__products = products
        Category.total_categories += 1
        Category.total_products += len(products)

    @property
    def products(self) -> str:
        """Возвращает форматированную строку со всеми товарами.

        Returns:
            Строка с информацией о товарах
        """
        return "\n".join(
            f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт."
            for p in self.__products
        )

    @property
    def product_list(self) -> List[Product]:
        """Возвращает список объектов товаров."""
        return self.__products

    def add_product(self, product: Product) -> None:
        """Добавляет товар в категорию.

        Args:
            product: Товар для добавления

        Raises:
            TypeError: Если передан не объект Product
        """
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product")
        self.__products.append(product)
        Category.total_products += 1

    @classmethod
    def from_json(cls, file_path: Path) -> 'Category':
        """Создает категорию из JSON-файла.

        Args:
            file_path: Путь к JSON-файлу

        Returns:
            Созданный объект Category
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        products = [
            Product(
                name=p['name'],
                description=p['description'],
                price=float(p['price']),
                quantity=int(p['quantity']),
            )
            for p in data['products']
        ]

        return cls(
            name=data['name'], description=data['description'], products=products
        )
