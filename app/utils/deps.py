from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer  
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password

