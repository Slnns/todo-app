from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
import crud
from database import engine, get_db

# Создаем таблицы
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API")

@app.get("/")
def root():
    return {
        "message": "Todo API работает!",
        "endpoints": {
            "GET /tasks": "Список всех задач (сортировка: новые/важные сверху)",
            "GET /tasks/{id}": "Задача по ID",
            "POST /tasks": "Создать задачу",
            "PUT /tasks/{id}": "Обновить задачу",
            "DELETE /tasks/{id}": "Удалить задачу"
        }
    }

@app.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(db: Session = Depends(get_db)):
    """Получить все задачи (сортировка: сначала новые, потом по приоритету)"""
    tasks = crud.get_tasks(db)
    return tasks

@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task

@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)

@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    updated_task = crud.update_task(db, task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return updated_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return {"message": "Задача удалена"}