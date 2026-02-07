import json
from typing import Any, Dict
from sqlmodel import Session, select
from datetime import datetime
from ..models.user import User
from ..models.task import Task
from .base import BaseMCPTool
from ..database.session import get_session


class DeleteTaskTool(BaseMCPTool):
    """
    MCP Tool for deleting a task from the user's list.
    """

    def get_name(self) -> str:
        return "delete_task"

    def get_description(self) -> str:
        return "Delete a task from the user's list"

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
                    "description": "The ID of the task to delete"
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

        # Get the task to delete
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

        # Delete the task
        session.delete(task)
        session.commit()

        # Prepare the response
        response = {
            "success": True,
            "message": "Task deleted successfully",
            "deleted_task_id": task_id
        }

        return response