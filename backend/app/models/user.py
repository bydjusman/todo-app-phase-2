from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import enum

if TYPE_CHECKING:
    from .todo import Todo


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class UserBase(SQLModel):
    username: str = Field(unique=True, nullable=False, max_length=50)
    email: str = Field(unique=True, nullable=False, max_length=100)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    role: UserRole = Field(default=UserRole.USER)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to todos
    todos: List["Todo"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str = Field(min_length=8)
    confirm_password: str


class UserUpdate(SQLModel):
    username: Optional[str] = Field(default=None, max_length=50)
    email: Optional[str] = Field(default=None, max_length=100)
    password: Optional[str] = Field(default=None, min_length=8)


class UserPublic(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime
    # Exclude hashed_password from public representation