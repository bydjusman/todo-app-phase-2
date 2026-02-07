from sqlalchemy import Column, String, Boolean, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from .database import Base, TimestampMixin, generate_uuid


class TaskPriority(str, enum.Enum):
    """Task priority levels."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Task(Base, TimestampMixin):
    """Task model for todo items."""

    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(String(36), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)
    description = Column(Text, nullable=False)
    priority = Column(
        Enum(TaskPriority, name="task_priority", create_type=False),
        default=TaskPriority.MEDIUM,
        nullable=False
    )
    is_completed = Column(Boolean, default=False, nullable=False)

    # Relationships
    user = relationship("User", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, description={self.description[:30]}..., priority={self.priority})>"
