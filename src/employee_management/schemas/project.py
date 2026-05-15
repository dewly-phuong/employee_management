from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from ..utils.enums import ProjectStatus
from datetime import datetime
from typing import List

class ProjectCreateRequest(BaseModel):
    name: str = Field(min_length=10, max_length=100)
    description: str = Field(max_length=255)
    description: str 
    status: str
    manager_id: UUID
    member_ids: List[UUID] = Field(default=[], description="")
    
class ProjectResponse(BaseModel):
    id: UUID
    name: str
    description: str
    status: ProjectStatus
    manager_id: UUID
    member_ids: List[UUID]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
class ProjectUpdateRequest(BaseModel):
    name: str
    description: str
    status: str
    manager_id: UUID
    member_ids: List[UUID]