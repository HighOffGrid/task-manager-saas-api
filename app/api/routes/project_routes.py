from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.schemas.project_schema import ProjectCreate
from app.db.database import get_db
from app.services import project_service

router = APIRouter(prefix="/projects")

@router.post("/")
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    return project_service.create_project_service(db, project)


@router.get("/")
def get_projects(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return project_service.get_projects_by_user(db, current_user.id)
