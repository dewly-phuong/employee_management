from fastapi import FastAPI
from contextlib import asynccontextmanager
from .api.router import api_router
from .core.database import db_manager
from .core.logging_config import setup_logging
from .core.exceptions import (
    NotFoundError,
    BadRequestError,
    AuthenticationError,
    not_found_exception_handler,
    bad_request_exception_handler,
    authentication_exception_handler
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup central logging
    setup_logging()
    # Initialize mongo database client
    await db_manager.connect()
    yield
    # Close Mongo database connection
    db_manager.close()

app = FastAPI(lifespan=lifespan)

# Register Exception Handlers
app.add_exception_handler(NotFoundError, not_found_exception_handler)
app.add_exception_handler(BadRequestError, bad_request_exception_handler)
app.add_exception_handler(AuthenticationError, authentication_exception_handler)

# Include main API router
app.include_router(api_router, prefix="/api/v1")
