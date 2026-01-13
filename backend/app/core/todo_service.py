from sqlmodel import Session, select
from ..models.todo import Todo, TodoCreate, TodoUpdate
from ..models.user import User
from typing import List, Optional
from datetime import datetime


class TodoService:
    """Service class for todo operations"""

    @staticmethod
    def create_todo(session: Session, todo_data: TodoCreate, user_id: int) -> Todo:
        """Create a new todo for a specific user"""
        # Create todo instance with provided data
        todo = Todo(
            title=todo_data.title,
            description=todo_data.description,
            completed=todo_data.completed,
            due_date=todo_data.due_date,
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

    @staticmethod
    def get_todo_by_id(session: Session, todo_id: int, user_id: int) -> Optional[Todo]:
        """Get a todo by ID for a specific user"""
        statement = select(Todo).where(Todo.id == todo_id).where(Todo.user_id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def get_all_todos(
        session: Session,
        user_id: int,
        offset: int = 0,
        limit: int = 50,
        completed: Optional[bool] = None
    ) -> List[Todo]:
        """Get all todos for a specific user with optional filtering and pagination"""
        statement = select(Todo).where(Todo.user_id == user_id)

        if completed is not None:
            statement = statement.where(Todo.completed == completed)

        statement = statement.offset(offset).limit(limit)
        return session.exec(statement).all()

    @staticmethod
    def update_todo(session: Session, todo_id: int, user_id: int, todo_data: TodoUpdate) -> Optional[Todo]:
        """Update a todo for a specific user"""
        todo = TodoService.get_todo_by_id(session, todo_id, user_id)
        if not todo:
            return None

        # Update only the fields that are provided
        # Convert to dict manually since SQLModel doesn't have dict() method
        update_data = {}
        if todo_data.title is not None:
            update_data['title'] = todo_data.title
        if todo_data.description is not None:
            update_data['description'] = todo_data.description
        if todo_data.completed is not None:
            update_data['completed'] = todo_data.completed
        if todo_data.due_date is not None:
            update_data['due_date'] = todo_data.due_date

        for field, value in update_data.items():
            setattr(todo, field, value)

        # Update the updated_at timestamp
        todo.updated_at = datetime.utcnow()

        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

    @staticmethod
    def delete_todo(session: Session, todo_id: int, user_id: int) -> bool:
        """Delete a todo for a specific user"""
        todo = TodoService.get_todo_by_id(session, todo_id, user_id)
        if not todo:
            return False

        session.delete(todo)
        session.commit()
        return True