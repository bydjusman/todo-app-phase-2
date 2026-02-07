import json
from typing import Any, Dict
from sqlmodel import Session, select
from ..models.user import User
from ..models.task import Task, TaskStatus
from .base import BaseMCPTool


class ListTasksTool(BaseMCPTool):
    """
    MCP Tool for listing tasks for a user with optional filtering.
    """

    def get_name(self) -> str:
        return "list_tasks"

    def get_description(self) -> str:
        return "Retrieve tasks for the user with optional filtering"

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The ID of the user whose tasks to retrieve"
                },
                "status": {
                    "type": "string",
                    "enum": ["pending", "completed", "all"],
                    "description": "Filter tasks by status. Default is 'all'"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of tasks to return. Default is 50"
                },
                "offset": {
                    "type": "integer",
                    "description": "Number of tasks to skip. Default is 0"
                }
            },
            "required": ["user_id"]
        }

    async def run(self, session: Session, **kwargs) -> Any:
        user_id = kwargs.get("user_id")
        status = kwargs.get("status", "all")
        limit = kwargs.get("limit", 50)
        offset = kwargs.get("offset", 0)

        # Validate inputs
        if not user_id:
            return {
                "success": False,
                "error": "user_id is required"
            }

        if limit <= 0 or limit > 1000:
            limit = 50  # Default to 50 if invalid

        if offset < 0:
            offset = 0

        # Verify user exists
        user = session.get(User, user_id)
        if not user:
            return {
                "success": False,
                "error": "User not found"
            }

        # Build query based on status filter
        query = select(Task).where(Task.user_id == user_id)

        if status != "all":
            task_status = TaskStatus.COMPLETED if status == "completed" else TaskStatus.PENDING
            query = query.where(Task.status == task_status)

        # Apply pagination
        query = query.offset(offset).limit(limit)

        # Execute query
        tasks = session.exec(query).all()

        # Convert tasks to dictionary format
        tasks_list = []
        for task in tasks:
            task_dict = {
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "status": task.status.value,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            if task.completed_at:
                task_dict["completed_at"] = task.completed_at.isoformat()

            tasks_list.append(task_dict)

        # Count total tasks for this user with the same filter
        count_query = select(Task).where(Task.user_id == user_id)
        if status != "all":
            task_status = TaskStatus.COMPLETED if status == "completed" else TaskStatus.PENDING
            count_query = count_query.where(Task.status == task_status)

        total_count = session.exec(count_query).count()

        # Prepare the response
        response = {
            "success": True,
            "tasks": tasks_list,
            "total_count": total_count
        }

        return response