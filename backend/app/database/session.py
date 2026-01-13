from sqlmodel import create_engine, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import os
from ..models.todo import Todo
from ..models.user import User


# Get database URL from environment, default to SQLite in memory for testing
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# For production, use PostgreSQL
if "postgresql" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
    )
else:
    # For SQLite (testing), use StaticPool
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


def create_db_and_tables():
    """Create database tables"""
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session"""
    with Session(engine) as session:
        yield session