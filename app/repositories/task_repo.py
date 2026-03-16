from  sqlalchemy.orm import Session
from app.models.task import Task

def create_task(db: Session, task):
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks(db: Session):
    return db.query(Task).all()