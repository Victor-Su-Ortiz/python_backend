from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional

from app.core.config import settings
from app.core.security import verify_password
from app.models.database import SessionLocal
from app.models.models import User
from app.schemas.schemas import TokenData

# OAuth2 scheme for token handling
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/token")


def get_db():
    """
    Dependency for database sessions.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dependency to get the current authenticated user.

    Args:
        db: Database session
        token: JWT token from request

    Returns:
        User: The authenticated user

    Raises:
        HTTPException: If authentication fails
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: Optional[str] = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    # Get the user from the database
    user = db.query(User).filter(User.username == token_data.username).first()

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency to get the current active user.

    Args:
        current_user: The authenticated user

    Returns:
        User: The active authenticated user

    Raises:
        HTTPException: If the user is inactive
    """
    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    """
    Authenticate a user by username and password.

    Args:
        db: Database session
        username: Username to check
        password: Password to verify

    Returns:
        User: The authenticated user or None if authentication fails
    """
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None

    return user
