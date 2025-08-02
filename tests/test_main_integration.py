import subprocess
import sys
from pathlib import Path


def test_run_main_py_as_script() -> None:
    """Интеграционный тест запуска main.py как скрипта."""
    base_dir = Path(__file__).parent.parent.resolve()
    json_path = base_dir / "data" / "example.json"
    main_module = "src.main"

    print(f"Запускаем main.py с: {json_path}")
    assert json_path.exists(), f"Файл не найден: {json_path}"

    result = subprocess.run(
        [sys.executable, "-m", main_module, str(json_path)],
        capture_output=True,
        text=True,
        timeout=10,
    )

    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)
    print("Код возврата:", result.returncode)

    assert result.returncode == 0, f"Process exited with {result.returncode}"
    assert "Категория" in result.stdout or "Ошибка" in result.stdout
