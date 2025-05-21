from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


# Task schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = Field(gt=0, lt=6, description="Priority between 1-5")
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    title: Optional[str] = None
    priority: Optional[int] = Field(None, gt=0, lt=6)
    completed: Optional[bool] = None


class Task(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True


class TaskInDB(Task):
    pass


# User with tasks
class UserWithTasks(User):
    tasks: List[Task] = []

    class Config:
        orm_mode = True
