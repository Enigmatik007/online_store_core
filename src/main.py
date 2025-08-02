import sys
import traceback
from pathlib import Path

from src.models import Category
from src.utils import load_data_from_json


def main(json_path: Path | None = None) -> int:
    if json_path is None:
        json_path = Path("data/example.json")
    print(f"Загрузка данных из: {json_path.resolve()}")

    try:
        categories = load_data_from_json(json_path)

        for category in categories:
            print(f"\nКатегория: {category.name}")
            print(f"Описание: {category.description}")
            print("Товары:")
            print(category.products)

        print(f"\nВсего категорий: {Category.total_categories}")
        print(f"Всего товаров: {Category.total_products}")

        return 0

    except Exception as e:
        print(f"Ошибка: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
