from datetime import datetime
from typing import Optional
from ..models.todo import Todo, TodoPublic


def todo_to_public(todo: Todo) -> TodoPublic:
    """Convert a Todo model to TodoPublic model"""
    return TodoPublic(
        id=todo.id,
        user_id=todo.user_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        due_date=todo.due_date,
        created_at=todo.created_at,
        updated_at=todo.updated_at
    )