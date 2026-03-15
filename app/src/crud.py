from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate, TaskUpdate

def get_tasks(db: Session):
    # Сортировка по дате создания (новые сверху) и приоритету
    return db.query(Task).order_by(Task.created_at.desc(), Task.priority.desc()).all()

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def create_task(db: Session, task: TaskCreate):
    db_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        completed=task.completed
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: TaskUpdate):
    db_task = get_task(db, task_id)
    if db_task:
        for key, value in task.dict(exclude_unset=True).items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False