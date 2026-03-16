from fastapi import APIRouter
from app.api.routes import auth_routes, task_routes, project_routes

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_routes.router)
api_router.include_router(task_routes.router)
api_router.include_router(project_routes.router)