from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi_pagination import Page
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler
from app.api.v1.api import api_router
from app.api.routes import auth_routes, task_routes, project_routes
from app.db.database import Base, engine
from app.core.log_middleware import LogMiddleware
from app.core.limiter import limiter

app = FastAPI(title="Task Manager SaaS")

add_pagination(app)

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(LogMiddleware)

Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)
app.include_router(task_routes.router)
app.include_router(project_routes.router)
app.include_router(api_router)