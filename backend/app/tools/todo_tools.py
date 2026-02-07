"""MCP Tools for Todo Operations"""
from typing import List, Optional, Dict, Any
from sqlmodel import Session
from pydantic import BaseModel
from ..models.todo import Todo, TodoCreate, TodoUpdate
from ..core.todo_service import TodoService
from ..database.session import get_session
from ..core.auth import get_current_user_from_token
from fastapi.security import OAuth2PasswordBearer
import uuid
from datetime import datetime


# Define Pydantic models for tool inputs/outputs
class AddTaskInput(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
    due_date: Optional[str] = None
    token: str


class AddTaskOutput(BaseModel):
    success: bool
    task_id: Optional[int] = None
    message: str


class ListTasksInput(BaseModel):
    token: str
    offset: Optional[int] = 0
    limit: Optional[int] = 50
    completed: Optional[bool] = None


class ListTasksOutput(BaseModel):
    success: bool
    tasks: List[Dict[str, Any]]
    total_count: int


class UpdateTaskInput(BaseModel):
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[str] = None
    token: str


class UpdateTaskOutput(BaseModel):
    success: bool
    message: str


class DeleteTaskInput(BaseModel):
    task_id: int
    token: str


class DeleteTaskOutput(BaseModel):
    success: bool
    message: str


class CompleteTaskInput(BaseModel):
    task_id: int
    token: str


class CompleteTaskOutput(BaseModel):
    success: bool
    message: str


class MCPTools:
    """MCP-compatible tools for todo operations"""

    @staticmethod
    def _get_user_from_token(token: str, session: Session):
        """Helper to get user from token"""
        user = get_current_user_from_token(token, session)
        if not user:
            raise ValueError("Invalid or expired token")
        return user

    @staticmethod
    def addtask01(input_data: AddTaskInput) -> AddTaskOutput:
        """
        Add a new task to the user's todo list

        Tool ID: addtask01 (alphanumeric, ≤9 chars, no hyphens/underscores)
        """
        with get_session() as session:
            try:
                user = MCPTools._get_user_from_token(input_data.token, session)

                # Prepare todo data
                todo_data = TodoCreate(
                    title=input_data.title,
                    description=input_data.description,
                    completed=input_data.completed,
                    due_date=input_data.due_date
                )

                # Create todo using service
                todo = TodoService.create_todo(session, todo_data, user.id)

                return AddTaskOutput(
                    success=True,
                    task_id=todo.id,
                    message=f"Task '{todo.title}' added successfully with ID {todo.id}"
                )
            except Exception as e:
                return AddTaskOutput(
                    success=False,
                    task_id=None,
                    message=f"Failed to add task: {str(e)}"
                )

    @staticmethod
    def listtask2(input_data: ListTasksInput) -> ListTasksOutput:
        """
        List tasks for the user with optional filtering

        Tool ID: listtask2 (alphanumeric, ≤9 chars, no hyphens/underscores)
        """
        with get_session() as session:
            try:
                user = MCPTools._get_user_from_token(input_data.token, session)

                # Get todos using service
                todos = TodoService.get_all_todos(
                    session,
                    user.id,
                    offset=input_data.offset,
                    limit=input_data.limit,
                    completed=input_data.completed
                )

                # Convert to dict format for output
                tasks = []
                for todo in todos:
                    task_dict = {
                        "id": todo.id,
                        "title": todo.title,
                        "description": todo.description,
                        "completed": todo.completed,
                        "due_date": todo.due_date.isoformat() if todo.due_date else None,
                        "created_at": todo.created_at.isoformat() if todo.created_at else None,
                        "updated_at": todo.updated_at.isoformat() if todo.updated_at else None
                    }
                    tasks.append(task_dict)

                return ListTasksOutput(
                    success=True,
                    tasks=tasks,
                    total_count=len(tasks)
                )
            except Exception as e:
                return ListTasksOutput(
                    success=False,
                    tasks=[],
                    total_count=0,
                    message=f"Failed to list tasks: {str(e)}"
                )

    @staticmethod
    def updatetsk(input_data: UpdateTaskInput) -> UpdateTaskOutput:
        """
        Update a specific task for the user

        Tool ID: updatetsk (alphanumeric, ≤9 chars, no hyphens/underscores)
        """
        with get_session() as session:
            try:
                user = MCPTools._get_user_from_token(input_data.token, session)

                # Prepare update data
                todo_data = TodoUpdate(
                    title=input_data.title,
                    description=input_data.description,
                    completed=input_data.completed,
                    due_date=input_data.due_date
                )

                # Update todo using service
                todo = TodoService.update_todo(session, input_data.task_id, user.id, todo_data)

                if todo:
                    return UpdateTaskOutput(
                        success=True,
                        message=f"Task {input_data.task_id} updated successfully"
                    )
                else:
                    return UpdateTaskOutput(
                        success=False,
                        message=f"Task {input_data.task_id} not found or doesn't belong to user"
                    )
            except Exception as e:
                return UpdateTaskOutput(
                    success=False,
                    message=f"Failed to update task: {str(e)}"
                )

    @staticmethod
    def complet01(input_data: CompleteTaskInput) -> CompleteTaskOutput:
        """
        Mark a task as completed

        Tool ID: complet01 (alphanumeric, ≤9 chars, no hyphens/underscores)
        """
        with get_session() as session:
            try:
                user = MCPTools._get_user_from_token(input_data.token, session)

                # Prepare update data to mark as completed
                todo_data = TodoUpdate(completed=True)

                # Update todo using service
                todo = TodoService.update_todo(session, input_data.task_id, user.id, todo_data)

                if todo:
                    return CompleteTaskOutput(
                        success=True,
                        message=f"Task {input_data.task_id} marked as completed"
                    )
                else:
                    return CompleteTaskOutput(
                        success=False,
                        message=f"Task {input_data.task_id} not found or doesn't belong to user"
                    )
            except Exception as e:
                return CompleteTaskOutput(
                    success=False,
                    message=f"Failed to complete task: {str(e)}"
                )

    @staticmethod
    def deletetsk(input_data: DeleteTaskInput) -> DeleteTaskOutput:
        """
        Delete a specific task for the user

        Tool ID: deletetsk (alphanumeric, ≤9 chars, no hyphens/underscores)
        """
        with get_session() as session:
            try:
                user = MCPTools._get_user_from_token(input_data.token, session)

                # Delete todo using service
                success = TodoService.delete_todo(session, input_data.task_id, user.id)

                if success:
                    return DeleteTaskOutput(
                        success=True,
                        message=f"Task {input_data.task_id} deleted successfully"
                    )
                else:
                    return DeleteTaskOutput(
                        success=False,
                        message=f"Task {input_data.task_id} not found or doesn't belong to user"
                    )
            except Exception as e:
                return DeleteTaskOutput(
                    success=False,
                    message=f"Failed to delete task: {str(e)}"
                )