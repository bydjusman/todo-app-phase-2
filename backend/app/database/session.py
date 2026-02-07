from sqlmodel import create_engine, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from ..models.todo import Todo
from ..models.user import User


def _normalize_database_url(raw: str) -> str:
    """
    Normalize DATABASE_URL from common copy-pastes.

    People often paste Neon connection like:
      DATABASE_URL=psql 'postgresql://...'
    This function extracts the real URL.
    """
    value = (raw or "").strip()
    if not value:
        return "sqlite:///./test.db"

    # Handle: psql 'postgresql://...'
    if value.startswith("psql"):
        # Best-effort: extract first quoted chunk
        first_quote = value.find("'")
        last_quote = value.rfind("'")
        if 0 <= first_quote < last_quote:
            extracted = value[first_quote + 1 : last_quote].strip()
            if extracted:
                return extracted

        # Or: psql postgresql://...
        parts = value.split()
        for part in parts:
            if part.startswith("postgresql://") or part.startswith("postgres://"):
                return part.strip()

    # Strip surrounding quotes
    if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
        value = value[1:-1].strip()

    return value


# Get database URL from environment, default to SQLite file for development
DATABASE_URL = _normalize_database_url(os.getenv("DATABASE_URL", "sqlite:///./test.db"))

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
    """Get database session with error handling"""
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        print(f"Database session error: {str(e)}")
        raise