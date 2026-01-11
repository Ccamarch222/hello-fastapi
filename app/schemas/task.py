from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    """Task base schema with common fields."""

    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    completed: bool = False
    priority: int = Field(default=0, ge=0, le=5)


class TaskCreate(TaskBase):
    """Schema for creating a new task."""

    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task. All fields optional."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[int] = Field(default=None, ge=0, le=5)


class TaskResponse(TaskBase):
    """Schema for task responses."""

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
