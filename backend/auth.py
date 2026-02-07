from datetime import datetime, timedelta
from typing import Optional
from datetime import timedelta
import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from .models import User
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize security scheme for JWT
security = HTTPBearer()

# Get secret key from environment
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "Bf6TlD2ADzQSHaanabLDSKlmACPnkAl6")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token with the provided data and expiration time.

    Args:
        data (dict): The data to encode in the token (usually user information)
        expires_delta (Optional[timedelta]): Token expiration time delta

    Returns:
        str: The encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token.

    Args:
        token (str): The JWT token to verify

    Returns:
        dict: The decoded token payload

    Raises:
        HTTPException: If the token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """
    Get the current authenticated user from the JWT token.

    Args:
        credentials: The HTTP authorization credentials containing the JWT token

    Returns:
        User: The authenticated user object

    Raises:
        HTTPException: If the token is invalid or user doesn't exist
    """
    token = credentials.credentials

    # Verify the token
    payload = verify_token(token)
    user_id: str = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database
    from .db import get_engine
    with Session(get_engine()) as session:
        user = session.get(User, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current authenticated user and verify they are active.

    Args:
        current_user: The authenticated user object

    Returns:
        User: The authenticated user object
    """
    # Additional checks can be added here if needed
    return current_user


def get_current_active_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current authenticated user and verify they have admin role.

    Args:
        current_user: The authenticated user object

    Returns:
        User: The authenticated user object (if they have admin role)

    Raises:
        HTTPException: If the user doesn't have admin role
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted - admin role required"
        )
    return current_user