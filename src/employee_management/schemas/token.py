from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field
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

    id: UUID
    email: EmailStr = Field(unique=True)
    username: str = Field(unique=True)
    full_name: str
    role: UserRole = UserRole.EMPLOYEE
    department: str
    skills: list[str] = []
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    """Data transfer object for login responses."""

    username: Optional[str] = None
