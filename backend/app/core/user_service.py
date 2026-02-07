from sqlmodel import Session
from typing import Optional
from ..models.user import User, UserCreate, UserUpdate
from .auth import get_password_hash, verify_password
from fastapi import HTTPException, status


class UserService:
    @staticmethod
    def create_user(session: Session, user_create: UserCreate) -> User:
        """Create a new user."""
        # Verify that passwords match
        if user_create.password != user_create.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )

        # Check if user with username already exists
        from sqlmodel import select
        existing_user_statement = select(User).where(User.username == user_create.username)
        existing_user = session.exec(existing_user_statement).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        # Check if user with email already exists
        existing_email_statement = select(User).where(User.email == user_create.email)
        existing_email = session.exec(existing_email_statement).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        # Ensure password is not too long for bcrypt (max 72 bytes)
        password_for_hashing = user_create.password[:72] if len(user_create.password) > 72 else user_create.password
        hashed_password = get_password_hash(password_for_hashing)
        db_user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        from sqlmodel import select
        statement = select(User).where(User.id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def get_user_by_username(session: Session, username: str) -> Optional[User]:
        """Get a user by username."""
        from sqlmodel import select
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """Get a user by email."""
        from sqlmodel import select
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

    @staticmethod
    def update_user(session: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update a user."""
        from sqlmodel import select
        db_user_statement = select(User).where(User.id == user_id)
        db_user = session.exec(db_user_statement).first()
        if not db_user:
            return None

        # Check if new username conflicts with existing users
        if user_update.username and user_update.username != db_user.username:
            existing_user_statement = select(User).where(User.username == user_update.username)
            existing_user = session.exec(existing_user_statement).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already registered"
                )

        # Check if new email conflicts with existing users
        if user_update.email and user_update.email != db_user.email:
            existing_email_statement = select(User).where(User.email == user_update.email)
            existing_email = session.exec(existing_email_statement).first()
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

        # Update user fields
        update_data = user_update.dict(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            # Ensure password is not too long for bcrypt (max 72 bytes)
            password_for_hashing = update_data["password"][:72] if len(update_data["password"]) > 72 else update_data["password"]
            update_data["hashed_password"] = get_password_hash(password_for_hashing)
            del update_data["password"]

        for field, value in update_data.items():
            setattr(db_user, field, value)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(session: Session, user_id: int) -> bool:
        """Delete a user."""
        from sqlmodel import select
        db_user_statement = select(User).where(User.id == user_id)
        db_user = session.exec(db_user_statement).first()
        if not db_user:
            return False

        session.delete(db_user)
        session.commit()
        return True

    @staticmethod
    def authenticate_user(session: Session, username: str, password: str) -> Optional[User]:
        """Authenticate a user by username/email and password."""
        from sqlmodel import select

        # First try to find by username
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()

        # If not found by username, try to find by email
        if not user:
            statement = select(User).where(User.email == username)  # 'username' parameter can be either username or email
            user = session.exec(statement).first()

        if not user or not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user