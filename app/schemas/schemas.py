from pydantic import BaseModel, Field
from typing import Optional


class TaskBase(BaseModel):
    """
    Schema for the task
    """

    title: str
    description: Optional[str] = None
