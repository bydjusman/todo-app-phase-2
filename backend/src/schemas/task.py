from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class TaskPriority(str, Enum):
    """Task priority levels."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskBase(BaseModel):
    """Base task schema."""

    description: str = Field(..., min_length=1, max_length=1000)


class TaskCreate(TaskBase):
    """Schema for creating a new task."""

    priority: TaskPriority = TaskPriority.MEDIUM
    category_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Buy groceries",
                "priority": "medium",
                "category_id": "uuid-here",
            }
        }


class TaskUpdate(BaseModel):
    """Schema for updating a task."""

    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    priority: Optional[TaskPriority] = None
    category_id: Optional[str] = None
    is_completed: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Buy organic groceries",
                "priority": "high",
            }
        }


class TaskResponse(TaskBase):
    """Schema for task response."""

    id: str
    user_id: str
    category_id: Optional[str]
    priority: TaskPriority
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskToggle(BaseModel):
    """Schema for toggling task completion."""

    is_completed: bool

    class Config:
        json_schema_extra = {
            "example": {
                "is_completed": True,
            }
        }
