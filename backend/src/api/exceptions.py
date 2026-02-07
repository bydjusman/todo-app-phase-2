from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Union
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)


class AppException(HTTPException):
    """Base application exception with custom error handling."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = None,
        headers: dict = None,
    ):
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers,
        )
        self.error_code = error_code or "app_error"


class NotFoundError(AppException):
    """Resource not found exception."""

    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found with id: {resource_id}",
            error_code="not_found",
        )


class ValidationAppError(AppException):
    """Validation error exception."""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="validation_error",
        )


class ConflictError(AppException):
    """Resource conflict exception."""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code="conflict",
        )


class RateLimitError(AppException):
    """Rate limit exceeded exception."""

    def __init__(self, detail: str = "Too many requests"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            error_code="rate_limit",
            headers={"Retry-After": "60"},
        )


async def app_exception_handler(request: Request, exc: AppException):
    """Handle custom application exceptions."""
    logger.warning(
        f"App exception: {exc.error_code} - {exc.detail}",
        extra={"path": request.url.path, "method": request.method}
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.detail,
            }
        },
        headers=exc.headers,
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle standard HTTP exceptions."""
    logger.warning(
        f"HTTP exception: {exc.status_code} - {exc.detail}",
        extra={"path": request.url.path, "method": request.method}
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "http_error",
                "message": exc.detail,
            }
        },
        headers=exc.headers,
    )


async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handle Pydantic validation errors."""
    logger.warning(
        f"Validation error: {exc.errors()}",
        extra={"path": request.url.path, "method": request.method}
    )

    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "validation_error",
                "message": "Request validation failed",
                "details": errors,
            }
        },
    )


async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(
        f"Unexpected error: {exc}",
        extra={"path": request.url.path, "method": request.method},
        exc_info=True,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "internal_error",
                "message": "An unexpected error occurred",
            }
        },
    )


def setup_exception_handlers(app):
    """Register all exception handlers with the FastAPI app."""
    from fastapi import FastAPI

    if isinstance(app, FastAPI):
        app.add_exception_handler(AppException, app_exception_handler)
        app.add_exception_handler(HTTPException, http_exception_handler)
        app.add_exception_handler(ValidationError, validation_exception_handler)
        app.add_exception_handler(Exception, global_exception_handler)
