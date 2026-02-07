import json
from typing import Any, Dict
from sqlmodel import Session, select
from datetime import datetime
from ..models.user import User
from ..models.task import Task, TaskStatus
from .base import BaseMCPTool
from ..database.session import get_session


class CompleteTaskTool(BaseMCPTool):
    """
    MCP Tool for marking a task as completed.
    """

    def get_name(self) -> str:
        return "complete_task"

    def get_description(self) -> str:
        return "Mark a task as completed"

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The ID of the user who owns the task"
                },
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to mark as completed"
                }
            },
            "required": ["user_id", "task_id"]
        }

    async def run(self, session: Session, **kwargs) -> Any:
        user_id = kwargs.get("user_id")
        task_id = kwargs.get("task_id")

        # Validate inputs
        if not user_id or not task_id:
            return {
                "success": False,
                "error": "user_id and task_id are required"
            }

        # Verify user exists
        user = session.get(User, user_id)
        if not user:
            return {
                "success": False,
                "error": "User not found"
            }

        # Get the task to complete
        task = session.get(Task, task_id)
        if not task:
            return {
                "success": False,
                "error": "Task not found"
            }

        # Verify that the task belongs to the user
        if task.user_id != user_id:
            return {
                "success": False,
                "error": "Unauthorized access: Task does not belong to user"
            }

        # Check if the task is already completed
        if task.status == TaskStatus.COMPLETED:
            return {
                "success": False,
                "error": "Task is already completed"
            }

        # Update the task status to completed
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.utcnow()
        task.updated_at = datetime.utcnow()

        # Commit changes
        session.add(task)
        session.commit()
        session.refresh(task)

        # Prepare the response
        response = {
            "success": True,
            "task": {
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "status": task.status.value,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
                "completed_at": task.completed_at.isoformat() if task.completed_at else None
            }
        }

        return response