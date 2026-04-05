from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP_SRC = str(ROOT / "app" / "src")
if APP_SRC not in sys.path:
    sys.path.insert(0, APP_SRC)

from schemas import TaskCreate, TaskUpdate


def test_task_create_defaults():
    task = TaskCreate(title="t1")
    assert task.priority == 1
    assert task.completed is False


def test_task_update_partial():
    up = TaskUpdate(title="x")
    assert up.model_dump(exclude_unset=True) == {"title": "x"}
