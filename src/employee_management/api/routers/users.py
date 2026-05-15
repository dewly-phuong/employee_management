from fastapi import APIRouter, Depends
from typing import List
import logging
from ...schemas.user import UserCreateRequest, UserResponse, UserUpdateRequest
from ...services.user_service import user_service
from ...services.authentication_service import get_current_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["User Enpoints"],
                   dependencies=[Depends(get_current_user)])


@router.post("/users")
async def create(user_create_request: UserCreateRequest) -> UserResponse:
    logger.info(f"USERS ROUTE: CREATE USER: {user_create_request.username}")
    return await user_service.create(user_create_request)

@router.get("/users/{id}")
async def get_one(id: str) -> UserResponse:
    logger.info(f"USERS/{id} ROUTE: FIND USER WITH ID:")
    return await user_service.get_by_id(id)

@router.get("/users")
async def get_all() -> List[UserResponse]:
    return await user_service.get_all()

@router.put("/users/{id}")
async def update(id: str, 
                 user_update_request: UserUpdateRequest
                 ) -> UserResponse:
    logger.info(f"USERS/{id} ROUTE: UPDATE USER BY ID: {user_update_request}")
    return await user_service.update(id, user_update_request)

@router.delete("/users/{id}")
async def delete(id: str) -> None:
    logger.info(f"USERS/{id} ROUTE: DELETE USER BY ID:")
    await user_service.delete(id)