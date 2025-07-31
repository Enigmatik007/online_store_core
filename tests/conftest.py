import json
from pathlib import Path

import pytest

from src.models import Category, Product


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
