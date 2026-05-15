from beanie import Document
from datetime import datetime, timezone
from pydantic import EmailStr, Field, field_validator
from uuid import UUID, uuid4
from ..utils.enums import UserRole


class User(Document):
    id: UUID = Field(default_factory=lambda: uuid4())
    email: EmailStr = Field(unique=True)
    username: str = Field(unique=True)
    password: str
    full_name: str
    role: UserRole = UserRole.EMPLOYEE
    department: str = Field(default="")
    skills: list[str] = []
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "users"

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: EmailStr) -> EmailStr:
        return email.lower()
