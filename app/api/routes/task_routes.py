from fastapi import APIRouter,  Depends
from sqlalchemy.orm import Session
from app.schemas.task_schema import TaskCreate, TaskResponse
from app.services import task_service
from app.db.database import SessionLocal, get_db
from app.core.dependencies import get_current_user
from fastapi_pagination import Page, paginate

router = APIRouter(prefix="/tasks")

@router.get("/", response_model=Page[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    tasks = task_service.get_tasks_by_user(db, current_user.id)

    return paginate(tasks)

@router.post("/")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return  task_service.create_task_service(db, task)           