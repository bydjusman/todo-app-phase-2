import json
from typing import Any, Dict
from sqlmodel import Session, select
from datetime import datetime
from ..models.user import User
from ..models.task import Task, TaskStatus
from .base import BaseMCPTool
from ..database.session import get_session
from sqlmodel import Session


class AddTaskTool(BaseMCPTool):
    """
    MCP Tool for adding a new task for a user.
    """

    def get_name(self) -> str:
        return "add_task"

    def get_description(self) -> str:
        return "Create a new task for the user"

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The ID of the user creating the task"
                },
                "title": {
                    "type": "string",
                    "description": "The title of the task"
                },
                "description": {
                    "type": "string",
                    "description": "Optional description of the task"
                },
                "due_date": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Optional due date for the task in ISO 8601 format"
                }
            },
            "required": ["user_id", "title"]
        }

    async def run(self, session: Session, **kwargs) -> Any:
        user_id = kwargs.get("user_id")
        title = kwargs.get("title")
        description = kwargs.get("description", "")
        due_date_str = kwargs.get("due_date")

        # Validate inputs
        if not user_id or not title:
            return {
                "success": False,
                "error": "user_id and title are required"
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

        # Create the task
        task = Task(
            title=title,
            description=description,
            status=TaskStatus.PENDING,
            user_id=user_id,
            due_date=due_date
        )

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