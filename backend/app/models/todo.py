from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class TodoBase(SQLModel):
    """Base model for Todo with common fields"""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    due_date: Optional[datetime] = Field(default=None)


class Todo(TodoBase, table=True):
    """Todo model for database storage"""
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="todos")


class TodoCreate(TodoBase):
    """Model for creating a new todo"""
    title: str = Field(..., min_length=1, max_length=255)
    completed: bool = False  # Default to False when creating
    # user_id is not included here as it will be set by the backend


class TodoUpdate(SQLModel):
    """Model for updating a todo (all fields optional)"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None


class TodoPublic(TodoBase):
    """Model for public todo representation"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime