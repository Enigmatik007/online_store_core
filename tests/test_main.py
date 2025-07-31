import pytest

import src.main
from src.models import Category, Product


def test_main_runs_without_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тестирует запуск main без ошибок."""

    def mock_load_data(file_path: str) -> list[Category]:
        product = Product("Test", "Desc", 10.0, 5)
        category = Category("TestCat", "Desc", [product])
        return [category]

    monkeypatch.setattr("src.main.load_data_from_json", mock_load_data)
    src.main.main()


def test_main_handles_exception(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Тестирует обработку исключений в main."""

    def mock_load_data_fail(file_path: str) -> None:
        raise RuntimeError("fail")

    monkeypatch.setattr("src.main.load_data_from_json", mock_load_data_fail)
    src.main.main()

    captured = capsys.readouterr()
    assert "Ошибка: fail" in captured.out
