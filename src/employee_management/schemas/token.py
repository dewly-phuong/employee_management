from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

from ..utils.enums import UserRole


class LoginRequest(BaseModel):
    """Data transfer object for login requests."""

    username: str
    password: str


class LoginResponse(BaseModel):
    """Data transfer object for login responses."""

    access_token: str
    token_type: str


class RegisterRequest(BaseModel):
    """Data transfer object for register requests."""

    username: str
    password: str
    email: EmailStr
    full_name: str


class CurrentUserResponse(BaseModel):
    """Data transfer object for current user responses."""

    username: str
    email: EmailStr
    full_name: str
    role: UserRole
    department: str
    skills: list[str]
    created_at: datetime
    updated_at: datetime


class TokenData(BaseModel):
    """Data transfer object for login responses."""

    username: Optional[str] = None
