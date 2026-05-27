from fastapi import APIRouter, Depends
from typing import List, Annotated
import logging
from ...services.authentication_service import get_current_user
from ...services.project_service import ProjectService
from ..dependencies import get_project_service
from ...schemas.project import ProjectCreateRequest, ProjectUpdateRequest, ProjectResponse

logger = logging.getLogger(__name__)


router = APIRouter(prefix=("/projects"),
                   tags=["Project Endpoints"],
                   dependencies=[Depends(get_current_user)])

@router.post("")
async def create(
    request: ProjectCreateRequest,
    project_service: Annotated[ProjectService, Depends(get_project_service)]
) -> ProjectResponse:
    logger.info(f"PROJECT ROUTE: CREATE PROJECT: {request.name}")
    return await project_service.create(request)

@router.get("/{id}")
async def get_one(
    id: str,
    project_service: Annotated[ProjectService, Depends(get_project_service)]
) -> ProjectResponse:
    logger.info(f"PROJECT/{id} ROUTE: FIND PROJECT WITH ID:")
    return await project_service.get_by_id(id)

@router.get("")
async def get_all(project_service: Annotated[ProjectService, Depends(get_project_service)]) -> List[ProjectResponse]:
    return await project_service.get_all()

@router.put("/{id}")
async def update(id: str, 
                 request: ProjectUpdateRequest,
                 project_service: Annotated[ProjectService, Depends(get_project_service)]
                 ) -> ProjectResponse:
    logger.info(f"PROJECT/{id} ROUTE: UPDATE PROJECT BY ID: {request}")
    return await project_service.update(id, request)

@router.delete("/{id}")
async def delete(id: str, project_service: Annotated[ProjectService, Depends(get_project_service)]) -> None:
    logger.info(f"PROJECT/{id} ROUTE: DELETE PROJECT BY ID:")
    await project_service.delete(id)