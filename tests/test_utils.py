import json
from pathlib import Path

from src.utils import load_data_from_json


def test_load_data_from_json(tmp_path: Path) -> None:
    """Тестирует загрузку данных из JSON файла."""
    # Создаем временный JSON-файл с тестовыми данными
    data = [
        {
            "name": "Category 1",
            "description": "Description 1",
            "products": [
                {
                    "name": "Product 1",
                    "description": "Desc 1",
                    "price": 10.0,
                    "quantity": 5,
                },
                {
                    "name": "Product 2",
                    "description": "Desc 2",
                    "price": 20.0,
                    "quantity": 3,
                },
            ],
        },
        {
            "name": "Category 2",
            "description": "Description 2",
            "products": [],
        },
    ]

    file_path = tmp_path / "data.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    categories = load_data_from_json(file_path)

    assert len(categories) == 2
    assert categories[0].name == "Category 1"
    # Проверяем список товаров через product_list
    assert len(categories[0].product_list) == 2
    assert categories[0].product_list[0].name == "Product 1"
    assert categories[0].product_list[0].price == 10.0
    assert categories[1].name == "Category 2"
    assert categories[1].product_list == []
