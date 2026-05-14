from beanie import Document, PydanticObjectId
from typing import Annotated
from datetime import datetime
from pydantic import EmailStr, Field, field_validator
from ..utils.enums import UserRole


class User(Document):
    id: PydanticObjectId
    email: EmailStr = Field(unique=True)
    username: str = Field(unique=True)
    password: str
    full_name: str
    role: UserRole = UserRole.EMPLOYEE
    department: str
    skills: list[str] = []
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    
    class Settings:
        name = "users"

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: EmailStr) -> EmailStr:
        return email.lower()
    

