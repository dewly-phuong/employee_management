from fastapi import APIRouter, Depends
from typing import List, Annotated
import logging
from ...schemas.user import UserCreateRequest, UserResponse, UserUpdateRequest
from ...services.user_service import UserService
from ..dependencies import get_user_service
from ...services.authentication_service import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(tags=["User Enpoints"],
                   dependencies=[Depends(get_current_user)])


@router.post("/users")
async def create(
    user_create_request: UserCreateRequest,
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> UserResponse:
    logger.info(f"USERS ROUTE: CREATE USER: {user_create_request.username}")
    return await user_service.create(user_create_request)

@router.get("/users/{id}")
async def get_one(
    id: str,
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> UserResponse:
    logger.info(f"USERS/{id} ROUTE: FIND USER WITH ID:")
    return await user_service.get_by_id(id)

@router.get("/users")
async def get_all(user_service: Annotated[UserService, Depends(get_user_service)]) -> List[UserResponse]:
    return await user_service.get_all()

@router.put("/users/{id}")
async def update(id: str, 
                 user_update_request: UserUpdateRequest,
                 user_service: Annotated[UserService, Depends(get_user_service)]
                 ) -> UserResponse:
    logger.info(f"USERS/{id} ROUTE: UPDATE USER BY ID: {user_update_request}")
    return await user_service.update(id, user_update_request)

@router.delete("/users/{id}")
async def delete(id: str, user_service: Annotated[UserService, Depends(get_user_service)]) -> None:
    logger.info(f"USERS/{id} ROUTE: DELETE USER BY ID:")
    await user_service.delete(id)