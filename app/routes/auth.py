from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils.deps import get_db
from app.core.security import get_password_hash
from app.models import models
from app.schemas import schemas

router = APIRouter(prefix="/auth", tags=["users"])


@router.post("/")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """register a new user"""
    user_db = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if user_db:
        return HTTPException(status_code=400, detail="username already exists")
    user_db = db.query(models.User).filter(models.User.email == user.email).first()
    if user_db:
        return HTTPException(status_code=400, detail="email already exists")

    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
