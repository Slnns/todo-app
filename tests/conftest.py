from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
APP_SRC = str(ROOT / "app" / "src")
if APP_SRC not in sys.path:
    sys.path.insert(0, APP_SRC)


@pytest.fixture(scope="module")
def test_app():
    import models

    with patch.object(models.Base.metadata, "create_all", return_value=None):
        import main

        yield main.app
        main.app.dependency_overrides.clear()


@pytest.fixture(scope="module")
def client(test_app):
    with TestClient(test_app) as c:
        yield c
