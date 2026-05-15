from beanie import Document
from datetime import datetime, timezone
from pydantic import Field
from typing import List
from uuid import UUID, uuid4
from ..utils.enums import ProjectStatus


class Project(Document):
    id: UUID = Field(default_factory=lambda: uuid4())
    name: str = Field(description="")
    description: str = Field(description="")
    status: ProjectStatus = Field(default=ProjectStatus.PLANNING,description="")
    manager_id: UUID = Field(description="")
    member_ids: List[UUID] = Field(default=[], description="")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "projects"
