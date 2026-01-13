import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database.session import create_db_and_tables
from backend.app.models.user import User
from backend.app.core.user_service import UserService
from sqlmodel import Session, select
from backend.app.database.session import engine

def init_db():
    print("Creating database tables...")
    create_db_and_tables()

    # Check if admin user exists
    with Session(engine) as session:
        statement = select(User).where(User.username == "admin")
        user = session.exec(statement).first()

        if not user:
            from backend.app.models.user import UserCreate
            # Create default admin user
            user_create = UserCreate(
                username="admin",
                email="admin@example.com",
                password="password123",
                confirm_password="password123"
            )

            try:
                created_user = UserService.create_user(session, user_create)
                print(f"Default admin user created: {created_user.username}")
            except Exception as e:
                print(f"Error creating default user: {e}")
        else:
            print("Admin user already exists")

    print("Database initialization complete!")

if __name__ == "__main__":
    init_db()