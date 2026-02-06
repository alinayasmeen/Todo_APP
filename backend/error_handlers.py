"""
Error handling utilities for the Todo App API
Ensures proper error responses without information leakage about other users' data
"""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Union
import logging
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


# Set up logging for error tracking
logger = logging.getLogger(__name__)


class AppError(Exception):
    """Base application error class"""
    def __init__(self, message: str, error_code: str = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "APP_ERROR"


class AccessDeniedError(AppError):
    """Raised when user tries to access resources they don't have permission for"""
    def __init__(self, message: str = "Access denied"):
        super().__init__(message, "ACCESS_DENIED")


class DataNotFoundError(AppError):
    """Raised when requested data is not found"""
    def __init__(self, message: str = "Data not found"):
        super().__init__(message, "DATA_NOT_FOUND")


class ValidationError(AppError):
    """Raised when input validation fails"""
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, "VALIDATION_ERROR")


async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handle validation errors with appropriate responses"""
    logger.warning(f"Validation error for {request.url.path}: {exc.message}")

    return JSONResponse(
        status_code=422,
        content={
            "detail": "Invalid input data",
            "error_code": exc.error_code
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with appropriate responses"""
    # Log the full error for internal tracking
    logger.error(f"HTTP error {exc.status_code} for {request.url.path}: {exc.detail}")

    # Return generic error response without exposing internal details
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": get_safe_error_message(exc.status_code, exc.detail)
        }
    )


async def app_exception_handler(request: Request, exc: AppError):
    """Handle application-specific errors"""
    logger.error(f"Application error for {request.url.path}: {exc.message} (Code: {exc.error_code})")

    status_code = get_status_code_for_error(exc.error_code)
    return JSONResponse(
        status_code=status_code,
        content={
            "detail": get_safe_error_message(status_code, exc.message),
            "error_code": exc.error_code
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    # Log the full error for internal tracking (including traceback)
    logger.error(f"Unexpected error for {request.url.path}: {str(exc)}", exc_info=True)

    # Return generic error response without exposing internal details
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )


def get_safe_error_message(status_code: int, original_message: str) -> str:
    """
    Generate safe error messages that don't leak information about other users' data
    """
    if status_code == 404:
        # Instead of revealing whether a resource exists or not, use generic message
        return "Resource not found"
    elif status_code == 403:
        # Generic access denied message
        return "Access denied"
    elif status_code == 401:
        # Authentication failure
        return "Authentication required"
    elif status_code == 422:
        # Validation error - keep generic but helpful
        return "Invalid input data"
    else:
        # For other errors, return generic message
        return "Request could not be processed"


def get_status_code_for_error(error_code: str) -> int:
    """Map error codes to appropriate HTTP status codes"""
    error_to_status = {
        "ACCESS_DENIED": 403,
        "DATA_NOT_FOUND": 404,
        "VALIDATION_ERROR": 422,
        "AUTHENTICATION_ERROR": 401
    }

    return error_to_status.get(error_code, 500)


def handle_resource_not_found(resource_type: str, resource_id: Union[int, str]):
    """Helper to handle resource not found errors consistently"""
    raise HTTPException(
        status_code=404,
        detail=f"{resource_type} not found"
    )


def handle_access_denied(resource_type: str = "resource"):
    """Helper to handle access denied errors consistently"""
    raise HTTPException(
        status_code=403,
        detail=f"Access denied: You don't have permission to access this {resource_type}"
    )


def validate_task_ownership(task, user_id: str):
    """
    Validate that a task belongs to the authenticated user
    Raises HTTPException if validation fails, without revealing information about other users' data
    """
    if task.user_id != user_id:
        # Don't reveal that the task exists but belongs to someone else
        # Just return a 404 to prevent user enumeration
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


def validate_user_data_isolation(resource_user_id: str, authenticated_user_id: str, resource_type: str = "resource"):
    """
    Validate that a resource belongs to the authenticated user
    Raises HTTPException if validation fails, without revealing information about other users' data
    """
    if resource_user_id != authenticated_user_id:
        # Don't reveal that the resource exists but belongs to someone else
        # Just return a 404 to prevent user enumeration
        raise HTTPException(
            status_code=404,
            detail=f"{resource_type.capitalize()} not found"
        )


# Register error handlers with FastAPI app
def register_error_handlers(app):
    """
    Register error handlers with the FastAPI application
    """
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(AccessDeniedError, app_exception_handler)
    app.add_exception_handler(DataNotFoundError, app_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)