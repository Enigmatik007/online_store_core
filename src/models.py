"""Модуль моделей для работы с товарами и категориями."""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any


class Product:
    """Класс для представления товара в магазине."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """Инициализирует товар.

        Args:
            name: Название товара
            description: Описание товара
            price: Цена товара
            quantity: Количество товара

        Raises:
            ValueError: При некорректных цене или количестве
        """
        self._name = name
        self._description = description
        self._quantity = int(quantity)
        self.__price = float(price)  # По-настоящему приватный атрибут

        if self.__price <= 0:
            raise ValueError("Цена должна быть положительной")
        if self._quantity < 0:
            raise ValueError("Количество не может быть отрицательным")

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
        """Устанавливает цену с проверкой.

        Args:
            value: Новая цена

        Note:
            При снижении цены требует подтверждения
        """
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
        """Устанавливает количество товара.

        Args:
            value: Новое количество
        """
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
        """Создает новый товар или обновляет существующий.

        Args:
            data: Данные нового товара
            existing_products: Список существующих товаров

        Returns:
            Созданный или обновлённый товар

        Raises:
            ValueError: При отсутствии обязательных полей
        """
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
        """Инициализирует категорию.

        Args:
            name: Название категории
            description: Описание категории
            products: Список товаров
        """
        self.name = name
        self.description = description
        self.__products = list(products) if products else []
        Category.total_categories += 1
        Category.total_products += len(self.__products)

    @property
    def products(self) -> str:
        """Возвращает строку с товарами категории."""
        return "\n".join(
            f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт."
            for p in self.__products
        )

    @property
    def product_list(self) -> List[Product]:
        """Возвращает список товаров категории."""
        return self.__products

    def add_product(self, product: Product) -> None:
        """Добавляет товар в категорию.

        Args:
            product: Товар для добавления

        Raises:
            TypeError: Если передан не объект Product или его наследник
        """
        if not isinstance(product, Product):  # Явная проверка типа
            raise TypeError("Добавлять можно только Product и наследников")
        self.__products.append(product)
        Category.total_products += 1

    @classmethod
    def from_json(cls, file_path: Path) -> 'Category':
        """Создает категорию из JSON-файла.

        Args:
            file_path: Путь к JSON-файлу

        Returns:
            Созданная категория
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
