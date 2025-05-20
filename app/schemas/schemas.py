from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


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


class TaskResponse(TaskBase):
    """
    for the response
    """

    id: int
    created_at: datetime
    owner_id: int
    completed: bool = False
