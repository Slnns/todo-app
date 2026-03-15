from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = 1
    completed: bool = False


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    completed: Optional[bool] = None


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: int
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True
        # Задаем порядок полей при выводе
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Пример задачи",
                "description": "Описание задачи",
                "priority": 3,
                "completed": False,
                "created_at": "2026-03-04T12:00:00"
            }
        }