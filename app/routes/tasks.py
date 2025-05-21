from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.models import models
from app.schemas import schemas
from app.models import database
from app.utils.deps import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_task = models.Task()