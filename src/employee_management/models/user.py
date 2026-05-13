from beanie import Document, Indexed
from uuid import uuid4, UUID
from typing import Annotated
from datetime import datetime
from pydantic import EmailStr, Field, field_validator
from ..utils.enums import UserRole


class User(Document):
    id: UUID = Field(default_factory=uuid4)
    email: EmailStr = Field(unique=True)
    username: str = Field(unique=True)
    hashed_password: str
    full_name: str
    role: UserRole = UserRole.EMPLOYEE
    department: str
    skills: list[str] = []
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: EmailStr) -> EmailStr:
        return email.lower()
