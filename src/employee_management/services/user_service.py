from ..repositories.user_repository import user_repository
from ..repositories.irepository import IRepository
from ..schemas.user import UserCreateRequest, UserResponse, UserUpdateRequest
from typing import List
from uuid import UUID
from ..services.authentication_service import get_password_hash
from datetime import datetime, timezone
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserService():
    def __init__(self, repo: IRepository):
        logger.info("USERSERVICE: INITIALIZE USER SERVICE...")
        self.repo = repo
        
    async def create(self,
                          request: UserCreateRequest
                          ) -> UserResponse:
        logger.info("USERSERVICE: CREATE USER...")
        obj = request.model_dump()
        obj['password'] = get_password_hash(obj.pop('password'))
        obj['updated_at'] = datetime.now(timezone.utc)
        db_object = self.repo.model(**obj)
        return UserResponse.model_validate(await self.repo.create(db_object))
    
    async def get_me(self) -> UserResponse:
        pass
    
    async def get_by_id(self, id: str) -> UserResponse:
        logger.info("USERSERVICE: GET USER BY ID...")
        db_object = await self.repo.get_by_id(UUID(id))
        return UserResponse.model_validate(db_object)
    
    async def get_all(self) -> List[UserResponse]:
        logger.info("USERSERVICE: GET ALL USER...")
        users = await self.repo.get_all()
        return [UserResponse.model_validate(user) for user in users]
    
    async def update(self,
                     id: str,
                     request: UserUpdateRequest
                     ) -> UserResponse:
        logger.info("USERSERVICE: UPDATE USER BY ID...")
        update_data = request.model_dump(exclude_unset=True)
        if 'password' in update_data:
            update_data['password'] = get_password_hash(update_data.pop('password'))
        db_object = await self.repo.update_by_id(UUID(id), update_data)
        return UserResponse.model_validate(db_object)
    
    async def delete(self, id: str) -> None:
        logger.info("USERSERVICE: DELETE USER BY ID...")
        try:
            await self.repo.delete_by_id(UUID(id))
        except Exception as exc:
            raise ValueError from exc
    
user_service = UserService(user_repository)