from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str
    status: str
    project_id: int

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    project_id: int
    created_at: datetime

    class Config:
        from_attributes = True