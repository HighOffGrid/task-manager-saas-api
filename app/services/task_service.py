from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, APIRouter
from app.db.database import get_db
from app.models.task import Task
from app.models.project import Project
from app.repositories import task_repo
from app.core.dependencies import get_current_user
from app.services import task_service
from app.core.logger import logger

router = APIRouter(prefix="/tasks")

def create_task_service(db: Session, data):

    try:

        logger.info(f"Creating task for project {data.project_id}")

        project = db.query(Project).filter(Project.id == data.project_id).first()

        if not project:
            logger.warning(f"Project {data.project_id} not found")

            raise HTTPException(
                status_code=404,
                detail="Project not found"
            )

        task = Task(**data.model_dump())

        created_task = task_repo.create_task(db, task)

        logger.info(f"Task created successfully | id={created_task.id}")

        return created_task

    except Exception as e:

        logger.error(f"Error creating task: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
