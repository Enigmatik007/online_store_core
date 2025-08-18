"""Основной модуль приложения для работы с каталогом товаров."""

import argparse
import logging
import sys
import traceback
from pathlib import Path
from typing import Optional, List

from src.models import Category, Product
from src.utils import load_data_from_json

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Парсит аргументы командной строки.

    Returns:
        Объект с разобранными аргументами командной строки.
    """
    parser = argparse.ArgumentParser(description="Обработчик каталога товаров из JSON")
    parser.add_argument(
        "json_path",
        type=Path,
        nargs="?",
        default="data/example.json",
        help="Путь к JSON-файлу с данными",
    )
    parser.add_argument(
        "--demo", action="store_true", help="Запустить демонстрационные примеры"
    )
    return parser.parse_args()


def process_categories(categories: List[Category]) -> None:
    """Обрабатывает и выводит информацию о категориях.

    Args:
        categories: Список категорий для обработки
    """
    for category in categories:
        logger.info("\nКатегория: %s", category.name)
        logger.info("Описание: %s", category.description)
        logger.info("Товары:")
        logger.info(category.products)


def run_demo_examples() -> None:
    """Запускает демонстрационные примеры работы с продуктами."""
    logger.info("\n=== ДЕМОНСТРАЦИОННЫЕ ПРИМЕРЫ ===")

    product1 = Product(
        name="Samsung Galaxy S23 Ultra",
        description="256GB, Серый цвет, 200MP камера",
        price=180000.0,
        quantity=5,
    )
    product2 = Product(
        name="Iphone 15", description="512GB, Gray space", price=210000.0, quantity=8
    )
    product3 = Product(
        name="Xiaomi Redmi Note 11",
        description="1024GB, Синий",
        price=31000.0,
        quantity=14,
    )

    category = Category(
        name="Смартфоны",
        description="Смартфоны как средство коммуникации",
        products=[product1, product2, product3],
    )

    logger.info("\nИсходные товары:")
    logger.info(category.products)

    product4 = Product(
        name="55\" QLED 4K", description="Фоновая подсветка", price=123000.0, quantity=7
    )
    category.add_product(product4)
    logger.info("\nПосле добавления товара:")
    logger.info(category.products)


def main(json_path: Optional[Path] = None, run_demo: bool = False) -> int:
    """Точка входа в приложение.

    Args:
        json_path: Путь к JSON-файлу
        run_demo: Флаг запуска демо-режима

    Returns:
        Код возврата: 0 при успехе, 1 при ошибке
    """
    try:
        if json_path is None:
            args = parse_args()
            json_path = args.json_path
            run_demo = args.demo

        if run_demo:
            run_demo_examples()

        if json_path.exists():
            logger.info("\nЗагрузка данных из: %s", json_path.resolve())
            categories = load_data_from_json(json_path)
            process_categories(categories)
            logger.info("\nВсего категорий: %s", Category.total_categories)
            logger.info("Всего товаров: %s", Category.total_products)
        elif not run_demo:
            raise FileNotFoundError(f"Файл не найден: {json_path}")

        return 0
    except Exception as e:
        # Дополнительно печатаем сообщение об ошибке в stdout, чтобы тесты могли поймать
        print(f"Ошибка: {e}")
        logger.error("Ошибка: %s", e)
        logger.debug("Трассировка:\n%s", traceback.format_exc())
        return 1


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("shop.log")],
    )
    sys.exit(main())
