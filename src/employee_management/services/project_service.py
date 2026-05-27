from ..repositories.irepository import IRepository
from ..schemas.project import ProjectCreateRequest, ProjectResponse, ProjectUpdateRequest
from ..utils.enums import ProjectStatus
from typing import List
from uuid import UUID
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class ProjectService:
    def __init__(self, repo: IRepository):
        logger.info("PROJECTSERVICE: INITIALIZE PROJECT SERVICE...")
        self.repo = repo
        
    async def create(self,
                          request: ProjectCreateRequest
                          ) -> ProjectResponse:
        logger.info("PROJECTSERVICE: CREATE PROJECT...")
        obj = request.model_dump()
        obj['updated_at'] = datetime.now(timezone.utc)
        obj['status'] = ProjectStatus(obj['status'])
        db_object = self.repo.model(**obj)
        return ProjectResponse.model_validate(await self.repo.create(db_object))
    
    async def get_me(self) -> ProjectResponse:
        pass
    
    async def get_by_id(self, id: str) -> ProjectResponse:
        logger.info("PROJECTSERVICE: GET PROJECT BY ID...")
        db_object = await self.repo.get_by_id(UUID(id))
        return ProjectResponse.model_validate(db_object)
    
    async def get_all(self) -> List[ProjectResponse]:
        logger.info("PROJECTSERVICE: GET ALL PROJECT...")
        projects = await self.repo.get_all()
        return [ProjectResponse.model_validate(project) for project in projects]
    
    async def update(self,
                     id: str,
                     request: ProjectUpdateRequest
                     ) -> ProjectResponse:
        logger.info("PROJECTSERVICE: UPDATE PROJECT BY ID...")
        update_data = request.model_dump(exclude_unset=True)
        db_object = await self.repo.update_by_id(UUID(id), update_data)
        return ProjectResponse.model_validate(db_object)
    
    async def delete(self, id: str) -> None:
        logger.info("PROJECTSERVICE: DELETE PROJECT BY ID...")
        try:
            await self.repo.delete_by_id(UUID(id))
        except Exception as exc:
            raise ValueError from exc
        
