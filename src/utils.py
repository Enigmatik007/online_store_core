import json
from pathlib import Path
from typing import Any, Dict, List

from .models import Category, Product


def load_data_from_json(file_path: Path) -> List[Category]:
    """Загружает данные о категориях и товарах из JSON-файла."""
    with open(file_path, 'r', encoding='utf-8-sig') as f:  # <--- здесь
        data: List[Dict[str, Any]] = json.load(f)

    return [
        Category(
            name=category['name'],
            description=category['description'],
            products=[
                Product(
                    name=product['name'],
                    description=product['description'],
                    price=product['price'],
                    quantity=product['quantity'],
                )
                for product in category['products']
            ],
        )
        for category in data
    ]
