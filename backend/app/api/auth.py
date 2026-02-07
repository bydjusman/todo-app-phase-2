from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from datetime import timedelta
from typing import Dict
from ..database.session import get_session
from ..models.user import User, UserCreate, UserPublic
from ..core.auth import authenticate_user, create_access_token
from ..core.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/register", response_model=UserPublic)
async def register_user(user_create: UserCreate, session: Session = Depends(get_session)):
    """Register a new user."""
    try:
        user = UserService.create_user(session, user_create)
        return user
    except HTTPException:
        # Re-raise HTTP exceptions (like duplicate username/email) as-is
        raise
    except ValueError as e:
        # Handle value errors (like invalid input)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while registering user: {str(e)}"
        )


@router.post("/signup", response_model=UserPublic)
async def signup_user(user_create: UserCreate, session: Session = Depends(get_session)):
    """Sign up a new user."""
    try:
        user = UserService.create_user(session, user_create)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while signing up user: {str(e)}"
        )


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """Authenticate user and return access token."""
    try:
        user = authenticate_user(session, form_data.username, form_data.password)
        if not user:
            # Check if user exists by username or email to provide specific error
            from sqlmodel import select

            # Check by username
            user_by_username = session.exec(select(User).where(User.username == form_data.username)).first()
            # Check by email
            user_by_email = session.exec(select(User).where(User.email == form_data.username)).first()

            if not user_by_username and not user_by_email:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        access_token_expires = timedelta(minutes=30)  # 30 minutes default
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during login: {str(e)}"
        )


@router.post("/logout")
async def logout():
    """Logout user (client-side cleanup required)."""
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserPublic)
async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    """Get current user info."""
    from ..core.auth import get_current_user_from_token

    user = get_current_user_from_token(token, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user