from fastapi import APIRouter,  Depends
from sqlalchemy.orm import Session
from app.schemas.task_schema import TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service
from app.db.database import SessionLocal, get_db
from app.core.dependencies import get_current_user
from fastapi_pagination import Page, paginate
from typing import Any


router = APIRouter(tags=["Tasks"])

@router.get("/", response_model=Page[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)  # ← MUDEI pra Any
):
    tasks = task_service.get_all_tasks_service(db)
    return paginate(tasks)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)  # ← MUDEI pra Any
):
    return task_service.get_task_by_id_service(db, task_id)


@router.post("/")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return  task_service.create_task_service(db, task)           

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)):
    return task_service.update_task_service(db, task_id, data)


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.delete_task_service(db, task_id)
