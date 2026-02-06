from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Optional
from datetime import timedelta
from ..models import User, UserRead, UserCreate, UserLogin
from ..auth import create_access_token, get_current_user
from pydantic import BaseModel
import bcrypt

router = APIRouter()


class UserRegisterRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserRegisterRequest):
    """
    Register a new user account.

    Args:
        user_data: User registration data containing email, password, and optional name

    Returns:
        UserResponse: Contains JWT access token and user information

    Raises:
        HTTPException: If email already exists or invalid input data
    """
    from ..db import get_engine
    with Session(get_engine()) as session:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Hash the password
        hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())

        # Create new user with default role 'user'
        db_user = User(
            email=user_data.email,
            name=user_data.name,
            role="user",  # Default role is 'user'
            hashed_password=hashed_password.decode('utf-8')
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        # Create access token
        access_token_expires = timedelta(minutes=30)  # 30 minutes expiry
        access_token = create_access_token(
            data={"sub": db_user.id, "email": db_user.email},
            expires_delta=access_token_expires
        )

        return UserResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserRead(
                id=db_user.id,
                email=db_user.email,
                name=db_user.name,
                role=db_user.role,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at
            )
        )


@router.post("/login", response_model=UserResponse)
def login_user(user_data: UserLoginRequest):
    """
    Authenticate user and return JWT token.

    Args:
        user_data: User login data containing email and password

    Returns:
        UserResponse: Contains JWT access token and user information

    Raises:
        HTTPException: If credentials are invalid
    """
    from ..db import get_engine
    with Session(get_engine()) as session:
        # Find user by email
        db_user = session.exec(select(User).where(User.email == user_data.email)).first()

        if not db_user or not bcrypt.checkpw(user_data.password.encode('utf-8'),
                                           db_user.hashed_password.encode('utf-8')):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token_expires = timedelta(minutes=30)  # 30 minutes expiry
        access_token = create_access_token(
            data={"sub": db_user.id, "email": db_user.email},
            expires_delta=access_token_expires
        )

        return UserResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserRead(
                id=db_user.id,
                email=db_user.email,
                name=db_user.name,
                role=db_user.role,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at
            )
        )


@router.get("/profile", response_model=UserRead)
def get_profile(current_user: User = Depends(get_current_user)):
    """
    Get the profile of the currently authenticated user.

    Args:
        current_user: The authenticated user object

    Returns:
        UserRead: The user's profile information
    """
    return UserRead(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )


@router.post("/refresh")
def refresh_token(current_user: User = Depends(get_current_user)):
    """
    Refresh the user's access token.

    Args:
        current_user: The authenticated user object

    Returns:
        UserResponse: Contains new JWT access token and user information
    """
    # Create new access token
    access_token_expires = timedelta(minutes=30)  # 30 minutes expiry
    access_token = create_access_token(
        data={"sub": current_user.id, "email": current_user.email},
        expires_delta=access_token_expires
    )

    return UserResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserRead(
            id=current_user.id,
            email=current_user.email,
            name=current_user.name,
            role=current_user.role,
            created_at=current_user.created_at,
            updated_at=current_user.updated_at
        )
    )