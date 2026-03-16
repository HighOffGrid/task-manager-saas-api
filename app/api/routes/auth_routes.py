from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.limiter import limiter

from app.schemas.user_schemas import UserCreate, UserLogin
from app.services import user_service
from app.repositories import user_repo
from app.db.database import SessionLocal
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(db, user.email, user.password)


@router.post("/login")
@limiter.limit("5/minute")
def login(
    request: Request,
    data: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = user_repo.get_user_by_email(db, data.email)

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    access_token = create_access_token({"sub": db_user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh_token(refresh_token: str):

    payload = decode_token(refresh_token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    email = payload.get("sub")

    new_access_token = create_access_token({"sub": email})

    return {"access_token": new_access_token}