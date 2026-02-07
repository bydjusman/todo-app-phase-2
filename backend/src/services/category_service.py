from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from models.category import Category


class CategoryService:
    """Service for category business logic."""

    def __init__(self, db: AsyncSession, user_id: str):
        self.db = db
        self.user_id = user_id

    async def list_categories(self) -> List[Category]:
        """List all categories for user."""
        result = await self.db.execute(
            select(Category)
            .where(Category.user_id == self.user_id)
            .order_by(Category.name)
        )
        return list(result.scalars().all())

    async def get_category(self, category_id: str) -> Optional[Category]:
        """Get a single category by ID."""
        result = await self.db.execute(
            select(Category).where(
                Category.id == category_id,
                Category.user_id == self.user_id
            )
        )
        return result.scalar_one_or_none()

    async def create_category(self, name: str, color: str = "#3B82F6") -> Category:
        """Create a new category."""
        # Check for duplicate name
        existing = await self.get_by_name(name)
        if existing:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=400,
                detail="Category with this name already exists"
            )

        category = Category(
            user_id=self.user_id,
            name=name,
            color=color,
        )
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def get_by_name(self, name: str) -> Optional[Category]:
        """Get category by name for user."""
        result = await self.db.execute(
            select(Category).where(
                Category.name == name,
                Category.user_id == self.user_id
            )
        )
        return result.scalar_one_or_none()

    async def update_category(
        self,
        category_id: str,
        name: Optional[str] = None,
        color: Optional[str] = None,
    ) -> Optional[Category]:
        """Update a category."""
        category = await self.get_category(category_id)
        if not category:
            return None

        if name is not None:
            # Check for duplicate name
            existing = await self.get_by_name(name)
            if existing and existing.id != category_id:
                from fastapi import HTTPException
                raise HTTPException(
                    status_code=400,
                    detail="Category with this name already exists"
                )
            category.name = name

        if color is not None:
            category.color = color

        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def delete_category(self, category_id: str) -> bool:
        """Delete a category."""
        category = await self.get_category(category_id)
        if not category:
            return False

        await self.db.delete(category)
        await self.db.commit()
        return True
