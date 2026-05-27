from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

class NotFoundError(Exception):
    def __init__(self, detail: str):
        self.detail = detail

class BadRequestError(Exception):
    def __init__(self, detail: str):
        self.detail = detail

class AuthenticationError(Exception):
    def __init__(self, detail: str = "Could not validate credentials"):
        self.detail = detail

async def not_found_exception_handler(request: Request, exc: NotFoundError):
    logger.warning(f"Not Found Error: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.detail},
    )

async def bad_request_exception_handler(request: Request, exc: BadRequestError):
    logger.warning(f"Bad Request Error: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.detail},
    )
    
async def authentication_exception_handler(request: Request, exc: AuthenticationError):
    logger.warning(f"Authentication Error: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.detail},
        headers={"WWW-Authenticate": "Bearer"},
    )
