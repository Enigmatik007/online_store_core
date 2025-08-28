"""Модуль моделей для работы с товарами и категориями."""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any, Iterator


class Product:
    """Класс для представления товара в магазине."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """Инициализирует товар."""
        self._name = name
        self._description = description
        self._quantity = int(quantity)
        self.__price = float(price)

        if self.__price <= 0:
            raise ValueError("Цена должна быть положительной")
        if self._quantity < 0:
            raise ValueError("Количество не может быть отрицательным")

    def __str__(self) -> str:
        """Возвращает строковое представление товара."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: 'Product') -> float:
        """Складывает продукты по формуле: цена * количество."""
        if type(other) is not Product:
            raise TypeError("Можно складывать только объекты Product")
        return (self.price * self.quantity) + (other.price * other.quantity)

    @property
    def name(self) -> str:
        """Возвращает название товара."""
        return self._name

    @property
    def description(self) -> str:
        """Возвращает описание товара."""
        return self._description

    @property
    def price(self) -> float:
        """Возвращает цену товара."""
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        """Устанавливает цену с проверкой."""
        value = float(value)
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if value < self.__price:
            confirm = input("Подтвердите снижение цены (y/n): ").strip().lower()
            if confirm == "y":
                self.__price = value
        else:
            self.__price = value

    @property
    def quantity(self) -> int:
        """Возвращает количество товара."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        """Устанавливает количество товара."""
        self._quantity = int(value)

    def __repr__(self) -> str:
        """Возвращает строковое представление товара."""
        return (
            f"Product(name={self._name!r}, description={self._description!r}, "
            f"price={self.__price!r}, quantity={self._quantity!r})"
        )

    @classmethod
    def new_product(
        cls, data: Dict[str, Any], existing_products: Optional[List['Product']] = None
    ) -> 'Product':
        """Создает новый товар или обновляет существующий."""
        required = ("name", "description", "price", "quantity")
        missing = [k for k in required if k not in data]
        if missing:
            raise ValueError(f"Отсутствуют обязательные поля: {missing}")

        name = data["name"]
        description = data["description"]
        price = float(data["price"])
        quantity = int(data["quantity"])

        if existing_products:
            for existing in existing_products:
                if existing.name == name:
                    existing.quantity += quantity
                    if price > existing.price:
                        existing.price = price
                    return existing

        return cls(name=name, description=description, price=price, quantity=quantity)


class Category:
    """Класс для представления категории товаров."""

    total_categories = 0
    total_products = 0

    def __init__(
        self, name: str, description: str, products: Optional[List[Product]] = None
    ):
        """Инициализирует категорию."""
        self.name = name
        self.description = description
        self.__products = list(products) if products else []
        Category.total_categories += 1
        Category.total_products += len(self.__products)

    def __str__(self) -> str:
        """Возвращает строковое представление категории."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self) -> Iterator[Product]:
        """Возвращает итератор по товарам категории."""
        return CategoryIterator(self)

    @property
    def products(self) -> str:
        """Возвращает строку с товарами категории."""
        return "\n".join(str(p) for p in self.__products)

    @property
    def product_list(self) -> List[Product]:
        """Возвращает список товаров категории."""
        return self.__products

    def add_product(self, product: Product) -> None:
        """Добавляет товар в категорию."""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только Product или его наследников")
        self.__products.append(product)
        Category.total_products += 1

    @classmethod
    def from_json(cls, file_path: Path) -> 'Category':
        """Создает категорию из JSON-файла."""
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


class CategoryIterator:
    """Итератор по товарам категории."""

    def __init__(self, category: Category) -> None:
        """Инициализирует итератор."""
        self._category = category
        self._index = 0

    def __iter__(self) -> 'CategoryIterator':
        """Возвращает сам итератор."""
        return self

    def __next__(self) -> Product:
        """Возвращает следующий товар в категории."""
        if self._index < len(self._category.product_list):
            product = self._category.product_list[self._index]
            self._index += 1
            return product
        raise StopIteration


class Smartphone(Product):
    """Класс для представления смартфонов."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        """Инициализирует смартфон."""
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self) -> str:
        """Возвращает строковое представление смартфона."""
        price_str = f"{self.price:.0f}" if self.price.is_integer() else f"{self.price}"
        return f"{self.name}, {price_str} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: Product) -> float:
        """Складывает смартфоны по формуле: цена * количество."""
        if type(other) is not Smartphone:
            raise TypeError("Можно складывать только объекты Smartphone")
        return (self.price * self.quantity) + (other.price * other.quantity)


class LawnGrass(Product):
    """Класс для представления газонной травы."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: int,
        color: str,
    ):
        """Инициализирует газонную траву."""
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self) -> str:
        """Возвращает строковое представление газонной травы."""
        price_str = f"{self.price:.0f}" if self.price.is_integer() else f"{self.price}"
        return f"{self.name}, {price_str} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: Product) -> float:
        """Складывает газонную траву по формуле: цена * количество."""
        if type(other) is not LawnGrass:
            raise TypeError("Можно складывать только объекты LawnGrass")
        return (self.price * self.quantity) + (other.price * other.quantity)
