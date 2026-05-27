from fastapi import Depends
from typing import Annotated

from ..repositories.user_repository import UserRepository
from ..repositories.project_repository import ProjectRepository
from ..services.user_service import UserService
from ..services.project_service import ProjectService

def get_user_repository() -> UserRepository:
    return UserRepository()

def get_project_repository() -> ProjectRepository:
    return ProjectRepository()

def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserService:
    return UserService(repo)

def get_project_service(
    repo: Annotated[ProjectRepository, Depends(get_project_repository)]
) -> ProjectService:
    return ProjectService(repo)
