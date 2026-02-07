from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CategoryBase(BaseModel):
    """Base category schema."""

    name: str = Field(..., min_length=1, max_length=100)


class CategoryCreate(CategoryBase):
    """Schema for creating a new category."""

    color: Optional[str] = "#3B82F6"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Work",
                "color": "#3B82F6",
            }
        }


class CategoryUpdate(BaseModel):
    """Schema for updating a category."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    color: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Personal",
                "color": "#10B981",
            }
        }


class CategoryResponse(CategoryBase):
    """Schema for category response."""

    id: str
    user_id: str
    color: str
    created_at: datetime

    class Config:
        from_attributes = True
