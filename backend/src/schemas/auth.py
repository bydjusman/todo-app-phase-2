from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data."""

    user_id: Optional[str] = None
    email: Optional[str] = None
    exp: Optional[datetime] = None


class Message(BaseModel):
    """Schema for simple message responses."""

    message: str


class RefreshToken(BaseModel):
    """Schema for refresh token request."""

    refresh_token: str
