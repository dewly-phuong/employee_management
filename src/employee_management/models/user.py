from beanie import Document
from datetime import datetime, timezone
from pydantic import EmailStr, Field, field_validator, model_validator
from uuid import UUID, uuid4
from typing import Any
from ..utils.enums import UserRole


class User(Document):
    id: UUID = Field(default_factory=lambda: uuid4())
    email: EmailStr | None = Field(default=None, unique=True)
    username: str = Field(default=None, unique=True)
    password: str
    full_name: str | None = Field(default=None)
    role: UserRole = UserRole.EMPLOYEE
    department: str | None = Field(default=None)
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
    
    @model_validator(mode="before")
    @classmethod
    def handle_root_email(cls, data: Any) -> Any:
        # Kiểm tra nếu dữ liệu đầu vào là một dictionary
        if isinstance(data, dict):
            role = data.get("role")
            email = data.get("email")
            
            # Nếu là root và email trống/không truyền, gán email mặc định hợp lệ
            if role == UserRole.ADMIN and (not email or email == ""):
                data["email"] = "root@root.ai"
                
        return data
