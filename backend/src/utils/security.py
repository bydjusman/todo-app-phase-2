from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from enum import Enum

from config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenType(str, Enum):
    """Token types for authentication."""

    ACCESS = "access"
    REFRESH = "refresh"


class AuthErrorCode(str, Enum):
    """Authentication error codes."""

    INVALID_TOKEN = "invalid_token"
    EXPIRED_TOKEN = "expired_token"
    INSUFFICIENT_PERMISSIONS = "insufficient_permissions"
    USER_INACTIVE = "user_inactive"
    INVALID_CREDENTIALS = "invalid_credentials"


class AuthError(HTTPException):
    """Custom authentication error with error codes."""

    def __init__(
        self,
        error_code: AuthErrorCode,
        detail: str = None,
        headers: dict = None,
    ):
        status_code_map = {
            AuthErrorCode.INVALID_TOKEN: status.HTTP_401_UNAUTHORIZED,
            AuthErrorCode.EXPIRED_TOKEN: status.HTTP_401_UNAUTHORIZED,
            AuthErrorCode.INSUFFICIENT_PERMISSIONS: status.HTTP_403_FORBIDDEN,
            AuthErrorCode.USER_INACTIVE: status.HTTP_403_FORBIDDEN,
            AuthErrorCode.INVALID_CREDENTIALS: status.HTTP_401_UNAUTHORIZED,
        }

        super().__init__(
            status_code=status_code_map.get(error_code, status.HTTP_401_UNAUTHORIZED),
            detail=detail or error_code.value,
            headers=headers or {"WWW-Authenticate": "Bearer"},
        )

        self.error_code = error_code


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def create_token(
    data: dict,
    token_type: TokenType,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a JWT token with specified type."""

    # Set expiration based on token type
    if expires_delta is None:
        if token_type == TokenType.ACCESS:
            expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
        else:
            expires_delta = timedelta(days=settings.refresh_token_expire_days)

    # Prepare payload
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({
        "exp": expire,
        "type": token_type.value,
        "iat": datetime.now(timezone.utc),
    })

    # Encode token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )

    return encoded_jwt


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a JWT access token."""
    return create_token(data, TokenType.ACCESS, expires_delta)


def create_refresh_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a JWT refresh token."""
    return create_token(data, TokenType.REFRESH, expires_delta)


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token.

    Raises:
        AuthError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        # Verify token type
        token_type = payload.get("type")
        if token_type != TokenType.ACCESS.value:
            raise AuthError(
                error_code=AuthErrorCode.INVALID_TOKEN,
                detail="Invalid token type",
            )

        return payload

    except JWTError as e:
        if "Expired" in str(e):
            raise AuthError(
                error_code=AuthErrorCode.EXPIRED_TOKEN,
                detail="Token has expired",
            )
        raise AuthError(
            error_code=AuthErrorCode.INVALID_TOKEN,
            detail="Could not validate credentials",
        )


def decode_refresh_token(token: str) -> dict:
    """Decode and validate a refresh token."""

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        if payload.get("type") != TokenType.REFRESH.value:
            raise AuthError(
                error_code=AuthErrorCode.INVALID_TOKEN,
                detail="Invalid token type for refresh",
            )

        return payload

    except JWTError as e:
        if "Expired" in str(e):
            raise AuthError(
                error_code=AuthErrorCode.EXPIRED_TOKEN,
                detail="Refresh token has expired",
            )
        raise AuthError(
            error_code=AuthErrorCode.INVALID_TOKEN,
            detail="Could not validate credentials",
        )


def generate_secure_secret() -> str:
    """Generate a secure secret key for JWT."""
    import secrets
    return secrets.token_urlsafe(32)
