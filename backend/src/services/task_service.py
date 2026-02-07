from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from models.task import Task, TaskPriority
from schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """Service for task business logic."""

    def __init__(self, db: AsyncSession, user_id: str):
        self.db = db
        self.user_id = user_id

    async def list_tasks(
        self,
        category_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Task]:
        """List all tasks for user with optional filters."""
        query = select(Task).where(Task.user_id == self.user_id)

        if category_id:
            query = query.where(Task.category_id == category_id)

        if status == "active":
            query = query.where(Task.is_completed == False)
        elif status == "completed":
            query = query.where(Task.is_completed == True)

        query = query.order_by(Task.created_at.desc())

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_task(self, task_id: str) -> Optional[Task]:
        """Get a single task by ID."""
        result = await self.db.execute(
            select(Task).where(
                Task.id == task_id,
                Task.user_id == self.user_id
            )
        )
        return result.scalar_one_or_none()

    async def add_task(self, task_data: TaskCreate) -> Task:
        """Create a new task."""
        task = Task(
            user_id=self.user_id,
            description=task_data.description,
            priority=task_data.priority,
            category_id=task_data.category_id,
        )
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def update_task(self, task_id: str, task_data: TaskUpdate) -> Optional[Task]:
        """Update a task."""
        task = await self.get_task(task_id)
        if not task:
            return None

        if task_data.description is not None:
            task.description = task_data.description
        if task_data.priority is not None:
            task.priority = task_data.priority
        if task_data.category_id is not None:
            task.category_id = task_data.category_id
        if task_data.is_completed is not None:
            task.is_completed = task_data.is_completed

        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete_task(self, task_id: str) -> bool:
        """Delete a task."""
        task = await self.get_task(task_id)
        if not task:
            return False

        await self.db.delete(task)
        await self.db.commit()
        return True

    async def toggle_completed(self, task_id: str, is_completed: bool) -> Optional[Task]:
        """Toggle task completion status."""
        task = await self.get_task(task_id)
        if not task:
            return None

        task.is_completed = is_completed
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get_stats(self) -> dict:
        """Get task statistics."""
        from sqlalchemy import func

        # Total tasks
        total_result = await self.db.execute(
            select(func.count(Task.id)).where(Task.user_id == self.user_id)
        )
        total_tasks = total_result.scalar() or 0

        # Completed tasks
        completed_result = await self.db.execute(
            select(func.count(Task.id)).where(
                Task.user_id == self.user_id,
                Task.is_completed == True
            )
        )
        completed_tasks = completed_result.scalar() or 0

        # By priority
        high_result = await self.db.execute(
            select(func.count(Task.id)).where(
                Task.user_id == self.user_id,
                Task.priority == TaskPriority.HIGH
            )
        )
        medium_result = await self.db.execute(
            select(func.count(Task.id)).where(
                Task.user_id == self.user_id,
                Task.priority == TaskPriority.MEDIUM
            )
        )
        low_result = await self.db.execute(
            select(func.count(Task.id)).where(
                Task.user_id == self.user_id,
                Task.priority == TaskPriority.LOW
            )
        )

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "active_tasks": total_tasks - completed_tasks,
            "completion_percentage": round((completed_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0,
            "by_priority": {
                "high": high_result.scalar() or 0,
                "medium": medium_result.scalar() or 0,
                "low": low_result.scalar() or 0,
            },
        }
