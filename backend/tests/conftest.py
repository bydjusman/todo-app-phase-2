pytest_plugins = ("pytest_asyncio",)

"""Configuration for pytest fixtures and test setup."""
import asyncio
import os
import sys
import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

# Set the database url to a test database before importing the app
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

# Change to src directory for imports
os.chdir(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.getcwd())

from config import settings
from models.database import Base, get_db
from main import app


# Create in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)

test_session_local = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session():
    """Create a fresh database session for each test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with test_session_local() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with database session override."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Return test user data for signup."""
    return {
        "email": "test@example.com",
        "password": "SecurePass123!",
        "confirm_password": "SecurePass123!",
    }


@pytest.fixture
def test_user_login():
    """Return test user login credentials."""
    return {
        "email": "test@example.com",
        "password": "SecurePass123!",
    }


# Import User model for sample_user fixture
from models.user import User
from app.core.auth import get_password_hash # Import get_password_hash

@pytest.fixture(scope="function")
async def sample_user(db_session: AsyncSession) -> User:
    """Create a sample user for testing purposes."""
    # Use a consistent test password
    test_password = "SecureTestPassword123!"
    hashed_test_password = get_password_hash(test_password)

    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hashed_test_password,
        role="user",
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user
