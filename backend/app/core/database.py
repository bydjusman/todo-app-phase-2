from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os


# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_chatbot.db")

# Create the engine
engine = create_engine(DATABASE_URL, echo=False)


def get_session() -> Generator[Session, None, None]:
    """Get a database session."""
    with Session(engine) as session:
        yield session


# Create a session factory
SessionLocal = sessionmaker(bind=engine, class_=Session)


def create_tables():
    """Create all tables in the database."""
    from backend.app.models.user import User
    from backend.app.models.task import Task
    from backend.app.models.conversation import Conversation
    from backend.app.models.conversation_entry import ConversationEntry

    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(bind=engine)


# Export the engine for use in other modules
__all__ = ["engine", "get_session", "SessionLocal", "create_tables"]