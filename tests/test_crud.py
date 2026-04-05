from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parent.parent
APP_SRC = str(ROOT / "app" / "src")
if APP_SRC not in sys.path:
    sys.path.insert(0, APP_SRC)

from crud import create_task, delete_task, get_task, get_tasks, update_task
from models import Task
from schemas import TaskCreate, TaskUpdate


def _fake_task(**kwargs):
    defaults = {
        "id": 1,
        "title": "a",
        "description": None,
        "priority": 2,
        "completed": False,
        "created_at": datetime.now(timezone.utc),
    }
    defaults.update(kwargs)
    t = Task(title=defaults["title"], description=defaults["description"], priority=defaults["priority"], completed=defaults["completed"])
    for k, v in defaults.items():
        setattr(t, k, v)
    return t


def test_get_tasks_orders_and_returns_rows():
    db = MagicMock()
    rows = [_fake_task(id=2), _fake_task(id=1)]
    db.query.return_value.order_by.return_value.all.return_value = rows

    assert get_tasks(db) == rows


def test_get_task_found():
    db = MagicMock()
    row = _fake_task()
    db.query.return_value.filter.return_value.first.return_value = row

    assert get_task(db, 99) is row


def test_create_task_commits():
    db = MagicMock()
    payload = TaskCreate(title="ttl", description="d", priority=3)

    created = create_task(db, payload)

    assert db.add.called
    assert db.commit.called
    assert db.refresh.called
    assert isinstance(created, Task)
    assert created.title == "ttl"


def test_update_task_applies_partial_fields():
    db = MagicMock()
    existing = _fake_task(id=1, title="old", priority=1)
    db.query.return_value.filter.return_value.first.return_value = existing

    assert update_task(db, 1, TaskUpdate(title="new")) is existing

    assert existing.title == "new"
    assert db.commit.called


def test_delete_task_true_when_exists():
    db = MagicMock()
    existing = _fake_task(id=5)
    db.query.return_value.filter.return_value.first.return_value = existing

    assert delete_task(db, 5) is True
    assert db.delete.called


def test_delete_task_false_when_missing():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    assert delete_task(db, 10) is False
