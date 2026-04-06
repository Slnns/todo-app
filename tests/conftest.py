from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
#Определяем, где корень проекта
ROOT = Path(__file__).resolve().parent.parent
#Формируем путь к папке с кодом
APP_SRC = str(ROOT / "app" / "src")
#Добавляем в пути поиска Python
if APP_SRC not in sys.path:
    sys.path.insert(0, APP_SRC)


@pytest.fixture(scope="module")
#создает приложение
def test_app():
    import models

    with patch.object(models.Base.metadata, "create_all", return_value=None):
        import main
        #временно подменяем метод create_all, он ничего не делает и возвращает None

        yield main.app
        #из-за patch это не создаёт таблицы в реальной БД
        main.app.dependency_overrides.clear()


@pytest.fixture(scope="module")
#создает клиента
def client(test_app):
    with TestClient(test_app) as c:
        yield c
