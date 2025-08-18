import pytest
from unittest.mock import patch

from src.models import Category, Product
from src.main import main


def test_main_runs_without_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тестирует запуск main без ошибок."""

    def mock_load_data(file_path: str) -> list[Category]:
        product = Product("Test", "Desc", 10.0, 5)
        category = Category("TestCat", "Desc", [product])
        return [category]

    # Мокаем аргументы командной строки
    with patch('sys.argv', ['main.py', 'data/example.json']):
        monkeypatch.setattr("src.main.load_data_from_json", mock_load_data)
        exit_code = main()
        assert exit_code == 0


def test_main_handles_exception(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Тестирует обработку исключений в main."""

    def mock_load_data_fail(file_path: str) -> None:
        raise RuntimeError("fail")

    # Мокаем аргументы командной строки
    with patch('sys.argv', ['main.py', 'data/example.json']):
        monkeypatch.setattr("src.main.load_data_from_json", mock_load_data_fail)
        exit_code = main()
        captured = capsys.readouterr()
        assert "Ошибка: fail" in captured.out
        assert exit_code == 1
