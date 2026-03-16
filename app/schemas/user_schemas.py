from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    email: str
    password: str = Field(min_length=6, max_length=72)

class UserLogin(BaseModel):
    email: str
    password: str    