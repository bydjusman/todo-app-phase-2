import json
from typing import Any, Dict
from sqlmodel import Session, select
from datetime import datetime
from ..models.user import User
from ..models.task import Task, TaskStatus
from .base import BaseMCPTool
from ..database.session import get_session


class UpdateTaskTool(BaseMCPTool):
    """
    MCP Tool for updating an existing task for a user.
    """

    def get_name(self) -> str:
        return "update_task"

    def get_description(self) -> str:
        return "Update an existing task for the user"

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
                    "description": "The ID of the task to update"
                },
                "title": {
                    "type": "string",
                    "description": "New title for the task (optional)"
                },
                "description": {
                    "type": "string",
                    "description": "New description for the task (optional)"
                },
                "due_date": {
                    "type": "string",
                    "format": "date-time",
                    "description": "New due date for the task in ISO 8601 format (optional)"
                }
            },
            "required": ["user_id", "task_id"]
        }

    async def run(self, session: Session, **kwargs) -> Any:
        user_id = kwargs.get("user_id")
        task_id = kwargs.get("task_id")
        title = kwargs.get("title")
        description = kwargs.get("description")
        due_date_str = kwargs.get("due_date")

        # Validate inputs
        if not user_id or not task_id:
            return {
                "success": False,
                "error": "user_id and task_id are required"
            }

        # Parse due date if provided
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
            except ValueError:
                return {
                    "success": False,
                    "error": "Invalid due date format. Use ISO 8601 format."
                }

        # Verify user exists
        user = session.get(User, user_id)
        if not user:
            return {
                "success": False,
                "error": "User not found"
            }

        # Get the task to update
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

        # Update the task fields if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if due_date is not None:
            task.due_date = due_date

        # Update the updated_at timestamp
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
                "updated_at": task.updated_at.isoformat()
            }
        }

        return response