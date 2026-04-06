from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parent.parent
APP_SRC = str(ROOT / "app" / "src")
if APP_SRC not in sys.path:
    sys.path.insert(0, APP_SRC)

from database import get_db
from models import Task
from schemas import TaskCreate


def _fake_task_row(**kwargs):
    #принимает любые именованные аргументы
    defaults = {
        "id": 1,
        "title": "a",
        "description": None,
        "priority": 2,
        "completed": False,
        "created_at": datetime(2026, 1, 1, tzinfo=timezone.utc),
    }
    defaults.update(kwargs)
    t = Task(
        title=defaults["title"],
        description=defaults["description"],
        priority=defaults["priority"],
        completed=defaults["completed"],
    )
    #установка значений
    for k, v in defaults.items():
        setattr(t, k, v)
    return t


def _override_get_db(test_app, mock_db):
    def _gen():
        yield mock_db

    test_app.dependency_overrides[get_db] = _gen


def test_root_ok(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["message"] == "Todo API работает!"


def test_list_tasks_empty(test_app, client):
    mock_db = MagicMock()
    #настройка возврата пустого списка
    mock_db.query.return_value.order_by.return_value.all.return_value = []
    _override_get_db(test_app, mock_db)
    try:
        r = client.get("/tasks/")
        assert r.status_code == 200
        assert r.json() == []
    finally:
        test_app.dependency_overrides.clear()


def test_get_task_404(test_app, client):
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    _override_get_db(test_app, mock_db)
    try:
        r = client.get("/tasks/999")
        assert r.status_code == 404
    finally:
        test_app.dependency_overrides.clear()


def test_get_task_200(test_app, client):
    row = _fake_task_row(id=3)
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = row
    _override_get_db(test_app, mock_db)
    try:
        r = client.get("/tasks/3")
        assert r.status_code == 200
        body = r.json()
        assert body["id"] == 3
        assert body["title"] == "a"
    finally:
        test_app.dependency_overrides.clear()


def test_create_task_via_api(test_app, client):
    mock_db = MagicMock()

    def refresh_side_effect(obj):
        obj.id = 7
        obj.created_at = datetime(2026, 3, 4, 12, 0, tzinfo=timezone.utc)

    mock_db.refresh.side_effect = refresh_side_effect

    _override_get_db(test_app, mock_db)
    try:
        r = client.post("/tasks/", json=TaskCreate(title="api", priority=2).model_dump())
        assert r.status_code == 200
        assert r.json()["id"] == 7  # после refresh в crud
        assert r.json()["title"] == "api"
    finally:
        test_app.dependency_overrides.clear()


def test_update_task_404(test_app, client):
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    _override_get_db(test_app, mock_db)
    try:
        r = client.put("/tasks/1", json={"title": "x"})
        assert r.status_code == 404
    finally:
        test_app.dependency_overrides.clear()


def test_delete_task_404(test_app, client):
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    _override_get_db(test_app, mock_db)
    try:
        r = client.delete("/tasks/1")
        assert r.status_code == 404
    finally:
        test_app.dependency_overrides.clear()


def test_delete_task_200(test_app, client):
    row = _fake_task_row(id=1)
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = row
    _override_get_db(test_app, mock_db)
    try:
        r = client.delete("/tasks/1")
        assert r.status_code == 200
        assert r.json()["message"] == "Задача удалена"
    finally:
        test_app.dependency_overrides.clear()
