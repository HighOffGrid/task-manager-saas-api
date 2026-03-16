from sqlalchemy.orm import Session
from app.models.project import Project
from app.repositories import project_repo
from app.core.cache import redis_client
import json


def create_project_service(db: Session, data):
    project = Project(**data.model_dump())
    return project_repo.create_project(db, project)

def get_projects_by_user(db, user_id):

    cache_key = f"user_projects:{user_id}"

    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    projects = project_repo.get_projects_by_user(db, user_id)

    redis_client.set(cache_key, json.dumps(projects), ex=60)

    return projects