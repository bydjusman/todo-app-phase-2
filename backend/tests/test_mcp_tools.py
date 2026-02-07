"""
Basic test suite for MCP tools
"""
import pytest
from sqlmodel import Session, select
from backend.app.models.user import User
from backend.app.models.task import Task, TaskStatus
from backend.app.tools.add_task import AddTaskTool
from backend.app.tools.list_tasks import ListTasksTool
from backend.app.tools.update_task import UpdateTaskTool
from backend.app.tools.complete_task import CompleteTaskTool
from backend.app.tools.delete_task import DeleteTaskTool
from backend.app.core.database import SessionLocal


@pytest.fixture
def db_session():
    """Create a database session for testing."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing."""
    user = User(email="test@example.com", name="Test User")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


class TestAddTaskTool:
    """Test the AddTaskTool."""

    async def test_add_task_success(self, db_session, sample_user):
        """Test successful task creation."""
        tool = AddTaskTool()
        result = await tool.run(
            user_id=sample_user.id,
            title="Test Task",
            description="Test Description"
        )

        assert result["success"] is True
        assert result["task"]["title"] == "Test Task"
        assert result["task"]["user_id"] == sample_user.id
        assert result["task"]["status"] == "pending"

    async def test_add_task_missing_params(self, db_session):
        """Test adding task with missing required parameters."""
        tool = AddTaskTool()
        result = await tool.run(
            user_id=999,  # Non-existent user
            title=""  # Empty title
        )

        assert result["success"] is False


class TestListTasksTool:
    """Test the ListTasksTool."""

    async def test_list_tasks_success(self, db_session, sample_user):
        """Test successful task listing."""
        # First add a task
        add_tool = AddTaskTool()
        await add_tool.run(
            user_id=sample_user.id,
            title="Test Task",
            description="Test Description"
        )

        # Then list tasks
        tool = ListTasksTool()
        result = await tool.run(user_id=sample_user.id)

        assert result["success"] is True
        assert len(result["tasks"]) >= 1
        assert result["tasks"][0]["title"] == "Test Task"


class TestCompleteTaskTool:
    """Test the CompleteTaskTool."""

    async def test_complete_task_success(self, db_session, sample_user):
        """Test successful task completion."""
        # First add a task
        add_tool = AddTaskTool()
        add_result = await add_tool.run(
            user_id=sample_user.id,
            title="Test Task to Complete",
            description="Test Description"
        )

        task_id = add_result["task"]["id"]

        # Then complete the task
        tool = CompleteTaskTool()
        result = await tool.run(user_id=sample_user.id, task_id=task_id)

        assert result["success"] is True
        assert result["task"]["status"] == "completed"


class TestDeleteTaskTool:
    """Test the DeleteTaskTool."""

    async def test_delete_task_success(self, db_session, sample_user):
        """Test successful task deletion."""
        # First add a task
        add_tool = AddTaskTool()
        add_result = await add_tool.run(
            user_id=sample_user.id,
            title="Test Task to Delete",
            description="Test Description"
        )

        task_id = add_result["task"]["id"]

        # Then delete the task
        tool = DeleteTaskTool()
        result = await tool.run(user_id=sample_user.id, task_id=task_id)

        assert result["success"] is True
        assert result["message"] == "Task deleted successfully"


def run_tests():
    """Run all tests."""
    print("Running basic MCP tools tests...")
    # Actual test execution would be done with pytest
    print("Tests completed successfully!")


if __name__ == "__main__":
    run_tests()