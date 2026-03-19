from fastapi import FastAPI
from fastapi_pagination import add_pagination
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler
from app.api.routes.task_routes import router as task_router
from app.api.v1.api import api_router
from app.db.database import Base, engine
from app.core.log_middleware import LogMiddleware
from app.core.limiter import limiter

app = FastAPI(title="Task Manager SaaS")

@app.get("/")
def read_root():
    return {"message": "API running"}

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(LogMiddleware)

Base.metadata.create_all(bind=engine)

app.include_router(task_router, prefix="/tasks", tags=["Tasks"])

add_pagination(app)