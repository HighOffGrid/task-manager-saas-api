from fastapi import HTTPException
from sqlalchemy.orm import Session
import logging
from app.models.task import Task
from app.models.project import Project
from app.repositories import task_repo
from app.core.logger import logger

logger = logging.getLogger(__name__)

def get_all_tasks_service(db: Session):
    logger.info("Listing all tasks")
    return db.query(Task).all()

def get_task_by_id_service(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task
def create_task_service(db: Session, data):
    try:
        logger.info(f"Creating task for project {data.project_id}")

        project = db.query(Project).filter(Project.id == data.project_id).first()

        if not project:
            logger.warning(f"Project {data.project_id} not found")
            raise HTTPException(status_code=404, detail="Project not found")

        task = Task(**data.model_dump())
        created_task = task_repo.create_task(db, task)

        logger.info(f"Task created successfully | id={created_task.id}")
        return created_task

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


def update_task_service(db: Session, task_id: int, data):
    try:
        logger.info(f"Updating task | id={task_id}")

        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            logger.warning(f"Task not found | id={task_id}")
            raise HTTPException(status_code=404, detail="Task not found")

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(task, field, value)

        db.commit()
        db.refresh(task)

        logger.info(f"Task updated successfully | id={task_id}")
        return task

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


def delete_task_service(db: Session, task_id: int):
    try:
        logger.info(f"Deleting task | id={task_id}")

        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            logger.warning(f"Task not found | id={task_id}")
            raise HTTPException(status_code=404, detail="Task not found")

        db.delete(task)
        db.commit()

        logger.info(f"Task deleted successfully | id={task_id}")
        return {"message": "Task deleted successfully"}
    

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting task: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    

def get_all_tasks_service(db: Session):
    try:
        logger.info("Listing all tasks")
        tasks = db.query(Task).all()
        return tasks

    except Exception as e:
        logger.error(f"Error listing tasks: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")