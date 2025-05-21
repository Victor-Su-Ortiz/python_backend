from ast import mod
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.models import models
from app.schemas import schemas
from app.models import database
from app.utils.deps import get_current_user, get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    create a new task
    """
    db_task = models.Task(**task.model_dump(), owner_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/", response_model=List[schemas.Task])
def get_tasks(
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    priority: Optional[int] = Query(gt=0, lt=6),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retreive the tasks for the current user

    Args:
        skip (int) number of tasks to skip
        limit (int): limit on number of tasks to include
        completed (bool): if the task if complete
        priority (int): priority of the tasks

    """
    query = db.query(models.Task).filter(models.Task.owner_id == current_user.id)
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
    if priority is not None:
        query = query.filter(models.Task.priority == priority)
    return query.offset(skip).limit(limit).all()
