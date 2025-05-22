from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.utils.deps import get_db, authenticate_user
from app.core.security import get_password_hash, create_access_token
from app.models import models
from app.schemas import schemas
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["users"])


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


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
