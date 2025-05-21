from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List


class TaskBase(BaseModel):
    """
    Schema for the task
    """

    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: int = Field(gt=0, lt=6, description=("Priority between 1-5"))


class TaskCreate(TaskBase):
    """
    class for creating a new task
    """


class Task(TaskBase):
    """
    for the response
    """

    id: int
    created_at: datetime
    owner_id: int
    completed: bool = False

    class Config:
        """
        the configuration
        """

        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    tasks: List[Task] = []
