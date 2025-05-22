from ast import mod
from webbrowser import get
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.models import models
from app.schemas import schemas
from app.models import database
from app.utils.deps import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


class MockUser:
    """Mock user model for testing purposes"""

    def __init__(self, id: int, username: str, email: str, is_active: bool = True):
        self.id = id
        self.username = username
        self.email = email
        self.is_active = is_active


def get_current_user() -> MockUser:
    """Mock getting the current user for testing purposes"""
    return MockUser(id=1, username="John Doe", email="johndoe@example.com")


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
    priority: Optional[int] = Query(None, gt=0, lt=6),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Retreive the tasks for the current user

    Args:
        skip (int) number of tasks to skip
        limit (int): limit on number of tasks to include
        completed (bool): if the task if complete
        priority (int): priority of the tasks

    Returns:
        tasks up to limit and args

    """
    query = db.query(models.Task).filter(models.Task.owner_id == current_user.id)
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
    if priority is not None:
        query = query.filter(models.Task.priority == priority)
    return query.offset(skip).limit(limit).all()


@router.get("/{task_id}", response_model=schemas.Task)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Get a specific task by ID

    Args:
        task_id (int): id of the task you want to fetch
    """
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id, models.Task.owner_id == current_user.id)
        .first()
    )
    if task is None:
        return HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int,
    update_data: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Update a task using a new task (put operation)
    """
    task_db = (
        db.query(models.Task)
        .filter(models.Task.id == task_id, models.Task.owner_id == current_user.id)
        .first()
    )

    if task_db is None:
        return HTTPException(status_code=404, detail="task not found")

    task_update = update_data.model_dump(exclude_unset=True)
    for key, value in task_update.items():
        setattr(task_db, key, value)
    db.commit()
    db.refresh(task_db)
    return task_db


@router.patch("/{task_id}/complete", response_model=schemas.Task)
def complete_task(
    task_id: int,
    db: Session = Depends(get_current_user),
    current_user: models.User = Depends(get_current_user),
):
    task_db = (
        db.query(models.Task)
        .filter(models.Task.id == task_id, models.Task.owner_id == current_user.id)
        .first()
    )

    if task_db is None:
        return HTTPException(status_code=404, detail="task not found")
    
