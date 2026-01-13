from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer
from ..database.session import get_session
from ..models.todo import Todo, TodoCreate, TodoUpdate, TodoPublic
from ..core.todo_service import TodoService
from ..core.utils import todo_to_public
from ..core.auth import get_current_user_from_token

router = APIRouter(prefix="/todos", tags=["todos"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    """Dependency to get the current authenticated user."""
    user = get_current_user_from_token(token, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.get("/", response_model=List[TodoPublic])
async def get_todos(
    offset: int = 0,
    limit: int = 50,
    completed: Optional[bool] = None,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all todos for the current user with optional filtering and pagination"""
    if limit > 100:
        limit = 100  # Enforce maximum limit

    todos = TodoService.get_all_todos(session, current_user.id, offset=offset, limit=limit, completed=completed)

    # Convert to public model to ensure consistent response format
    return [todo_to_public(todo) for todo in todos]


@router.get("/{todo_id}", response_model=TodoPublic)
async def get_todo(todo_id: int, current_user = Depends(get_current_user), session: Session = Depends(get_session)):
    """Get a specific todo by ID for the current user"""
    todo = TodoService.get_todo_by_id(session, todo_id, current_user.id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo_to_public(todo)


@router.post("/", response_model=TodoPublic, status_code=status.HTTP_201_CREATED)
async def create_todo(todo_data: TodoCreate, current_user = Depends(get_current_user), session: Session = Depends(get_session)):
    """Create a new todo for the current user"""
    todo = TodoService.create_todo(session, todo_data, current_user.id)
    return todo_to_public(todo)


@router.put("/{todo_id}", response_model=TodoPublic)
async def update_todo(todo_id: int, todo_data: TodoUpdate, current_user = Depends(get_current_user), session: Session = Depends(get_session)):
    """Update all fields of a specific todo for the current user"""
    todo = TodoService.update_todo(session, todo_id, current_user.id, todo_data)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo_to_public(todo)


@router.patch("/{todo_id}", response_model=TodoPublic)
async def partial_update_todo(todo_id: int, todo_data: TodoUpdate, current_user = Depends(get_current_user), session: Session = Depends(get_session)):
    """Update specific fields of a todo for the current user"""
    todo = TodoService.update_todo(session, todo_id, current_user.id, todo_data)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo_to_public(todo)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, current_user = Depends(get_current_user), session: Session = Depends(get_session)):
    """Delete a specific todo for the current user"""
    success = TodoService.delete_todo(session, todo_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return