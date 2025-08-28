# Online Store Core

Ядро интернет-магазина с системой управления товарами и категориями.

## 📦 Особенности

- Полностью типизированный код (Python 3.12+)
- Валидация данных при создании объектов
- Работа с JSON-файлами
- Поддержка категорий и товаров
- Автоматический подсчет статистики
- Абстрактный класс BaseProduct, обеспечивающий единый интерфейс для всех типов товаров.
- Конкретные классы: Product, Smartphone, LawnGrass — с полной реализацией методов.
- Миксин ReprMixin для автоматического логирования создания объектов.
- Поддержка сложения товаров по формуле: цена × количество.
- Валидация данных при создании (цена, количество).
- Гибкая система наследования и переопределения методов.

## 🛠️ Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/online-store-core.git
   cd online-store-core
   ```

2. Установите зависимости через Poetry:
   ```bash
   poetry install
   ```

3. Активируйте окружение:
   ```bash
   poetry shell
   ```

## 🚀 Использование

**Основные классы:**
```python
from src.models import Product, Category

# Создание товара
product = Product(
    name="iPhone 15",
    description="256GB, Space Gray",
    price=999.99,
    quantity=10
)

# Создание категории
category = Category(
    name="Smartphones",
    description="Mobile devices",
    products=[product]
)
```

**Загрузка из JSON:**
```python
from src.utils import load_data_from_json
from pathlib import Path

categories = load_data_from_json(Path("data/example.json"))
```

## 🧪 Тестирование

Запуск тестов с покрытием:
```bash
poetry run pytest --cov
```

Проверка типов:
```bash
poetry run mypy src/
```

Проверка стиля кода:
```bash
poetry run flake8 src/
poetry run black --check src/
```

## 📊 Статистика кода

- Покрытие тестами: **95%+**
- Типизация: **100%**
- Соответствие PEP 8: **100%**

## 📂 Структура проекта
```
online-store-core/
├── data/               # Данные (JSON-файлы)
├── src/                # Исходный код
│   ├── models.py       # Основные классы
│   ├── utils.py        # Вспомогательные функции
│   └── main.py         # Точка входа
├── tests/              # Тесты
├── .gitignore
├── pyproject.toml
└── README.md
```
