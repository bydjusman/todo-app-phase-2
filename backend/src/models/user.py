from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from models.database import Base, TimestampMixin, generate_uuid

class User(Base, TimestampMixin):
    """User model for authentication."""

    __tablename__ = "users"
    __table_args__ = {'extend_existing': True} 

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # Relationships - Sirf Class Name use karein lekin path ko avoid karein
    # back_populates wahi hona chahiye jo Task aur Category class mein define hai
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"