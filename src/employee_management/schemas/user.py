from pydantic import BaseModel, Field, EmailStr, ConfigDict
from uuid import UUID
from ..utils.enums import UserRole
from datetime import datetime

class UserCreateRequest(BaseModel):
    username: str = Field(min_length=5, max_length=20, unique=True)
    email: EmailStr = Field(unique=True)
    password: str
    full_name: str
    
class UserResponse(BaseModel):
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
    
class UserUpdateRequest(BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)
    full_name: str = Field(default=None)
    skill: str = Field(default=None)
