from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Task(SQLModel, table=True):
    """Task database model for task management."""

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Task fields
    title: str = Field(max_length=200)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    priority: int = Field(default=0, ge=0, le=5)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
