from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from ...schemas.token import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    CurrentUserResponse,
)
from ...services.authentication_service import get_current_user, login
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth")


@router.post("/login")
async def route_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> LoginResponse:
    logger.info(f"LOGGIN ROUTE: LOGIN ATTEMPT: {form_data.username}")
    login_request = LoginRequest(
        username=form_data.username, password=form_data.password
    )
    return await login(login_request)


@router.get("/me")
async def get_me(
    current_user: Annotated[CurrentUserResponse, Depends(get_current_user)],
) -> CurrentUserResponse:
    logger.info(f"LOGGIN ROUTE: GET CURRENT USER: {current_user.username}")
    return current_user

@router.post("/register")
async def register() -> bool:
    return {}


@router.post("/refresh")
async def refresh_token():
    pass
