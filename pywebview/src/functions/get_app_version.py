import tomllib
import os
import sys

def get_app_version() -> str:
    """
    Читает и возвращает версию приложения из pyproject.toml.
    Работает как до, так и после упаковки через PyInstaller.
    """
    # Определяем путь к pyproject.toml
    if hasattr(sys, "_MEIPASS"):
        # Если приложение упаковано, ищем файл в временной папке PyInstaller
        toml_path = os.path.join(sys._MEIPASS, "pyproject.toml")
    else:
        # В случае запуска из исходного кода, используем локальный путь
        dirname = os.path.dirname(__file__)
        toml_path = os.path.join(dirname, '../../pyproject.toml')

    try:
        with open(toml_path, "rb") as file:
            pyproject_data = tomllib.load(file)
            return pyproject_data["project"]["version"]
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {toml_path} не найден")
    except KeyError:
        raise KeyError("Не удалось найти секцию [project] или поле version")
    except Exception as e:
        raise RuntimeError(f"Ошибка при чтении {toml_path}: {e}")