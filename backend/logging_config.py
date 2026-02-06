import logging
import json
from datetime import datetime
from typing import Dict, Any
from pythonjsonlogger import jsonlogger
import sys
import os

class StructuredFormatter(jsonlogger.JsonFormatter):
    """
    Custom formatter that adds structured logging with consistent field names
    and additional contextual information.
    """

    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]) -> None:
        """
        Add custom fields to the log record.

        Args:
            log_record: Dictionary to populate with log fields
            record: Original LogRecord from logging module
            message_dict: Dictionary containing the log message
        """
        super().add_fields(log_record, record, message_dict)

        # Add timestamp in ISO format
        log_record['timestamp'] = datetime.fromtimestamp(record.created).isoformat()

        # Add log level
        log_record['level'] = record.levelname

        # Add service name
        log_record['service'] = 'todo-app-backend'

        # Add process information
        log_record['process_id'] = os.getpid()

        # Add thread information
        log_record['thread_name'] = record.threadName

        # Add module and function information
        log_record['module'] = record.module
        log_record['function'] = record.funcName
        log_record['line'] = record.lineno

        # Add request context if available
        if hasattr(record, 'request_id'):
            log_record['request_id'] = getattr(record, 'request_id', None)

        if hasattr(record, 'user_id'):
            log_record['user_id'] = getattr(record, 'user_id', None)

        if hasattr(record, 'endpoint'):
            log_record['endpoint'] = getattr(record, 'endpoint', None)


def setup_structured_logging(level: str = 'INFO') -> None:
    """
    Configure structured logging for the application.

    Args:
        level: Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    """
    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))

    # Clear any existing handlers
    root_logger.handlers.clear()

    # Create console handler with structured formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(StructuredFormatter(
        '%(timestamp)s %(level)s %(service)s %(message)s %(module)s %(function)s %(line)d',
        rename_fields={'message': 'msg'}
    ))

    # Add handler to root logger
    root_logger.addHandler(console_handler)

    # Configure specific loggers
    uvicorn_logger = logging.getLogger('uvicorn')
    uvicorn_logger.setLevel(getattr(logging, level.upper()))

    fastapi_logger = logging.getLogger('fastapi')
    fastapi_logger.setLevel(getattr(logging, level.upper()))

    # SQLAlchemy logger for database queries
    sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
    sqlalchemy_logger.setLevel(logging.WARNING)  # Set to WARNING to avoid verbose SQL logs


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    Args:
        name: Name of the logger

    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)


def log_api_request(
    logger: logging.Logger,
    method: str,
    endpoint: str,
    status_code: int,
    response_time: float,
    user_id: str = None,
    request_id: str = None
) -> None:
    """
    Log API request with structured format.

    Args:
        logger: Logger instance to use
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint
        status_code: HTTP response status code
        response_time: Time taken to process the request in seconds
        user_id: ID of the authenticated user (if any)
        request_id: Unique request identifier
    """
    extra = {
        'request_method': method,
        'endpoint': endpoint,
        'status_code': status_code,
        'response_time_ms': round(response_time * 1000, 2),
        'component': 'api'
    }

    if user_id:
        extra['user_id'] = user_id

    if request_id:
        extra['request_id'] = request_id

    logger.info(
        f"{method} {endpoint} {status_code} {round(response_time * 1000, 2)}ms",
        extra=extra
    )


def log_authentication_event(
    logger: logging.Logger,
    event_type: str,
    user_id: str = None,
    email: str = None,
    success: bool = True,
    details: str = None
) -> None:
    """
    Log authentication events with structured format.

    Args:
        logger: Logger instance to use
        event_type: Type of authentication event ('login', 'logout', 'token_validation', etc.)
        user_id: ID of the user involved
        email: Email of the user involved
        success: Whether the event was successful
        details: Additional details about the event
    """
    extra = {
        'event_type': event_type,
        'success': success,
        'component': 'auth'
    }

    if user_id:
        extra['user_id'] = user_id

    if email:
        extra['email'] = email

    if details:
        extra['details'] = details

    logger.info(
        f"Authentication {event_type}: {'success' if success else 'failure'}",
        extra=extra
    )


def log_security_event(
    logger: logging.Logger,
    event_type: str,
    user_id: str = None,
    ip_address: str = None,
    endpoint: str = None,
    details: str = None
) -> None:
    """
    Log security-related events with structured format.

    Args:
        logger: Logger instance to use
        event_type: Type of security event
        user_id: ID of the user involved (if any)
        ip_address: IP address of the request
        endpoint: Endpoint where the event occurred
        details: Additional details about the event
    """
    extra = {
        'event_type': event_type,
        'component': 'security'
    }

    if user_id:
        extra['user_id'] = user_id

    if ip_address:
        extra['ip_address'] = ip_address

    if endpoint:
        extra['endpoint'] = endpoint

    if details:
        extra['details'] = details

    logger.warning(
        f"Security event: {event_type}",
        extra=extra
    )


# Initialize logging when module is imported
setup_structured_logging()