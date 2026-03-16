from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories import user_repo
from app.workers.tasks import send_email_task
from app.core.security import hash_password


def register_user(db: Session, email: str, password: str):

    # verificar se usuário já existe
    existing_user = user_repo.get_user_by_email(db, email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    # hash da senha
    hashed_password = hash_password(password)

    # criar usuário
    user = user_repo.create_user(db, email, hashed_password)

    # tarefa em background
    send_email_task.delay(email)

    return user