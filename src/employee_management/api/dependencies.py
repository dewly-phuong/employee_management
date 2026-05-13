from fastapi import Request, Depends
from typing import Annotated, Any
from ..services.user_service import UserService
from ..database import MongoDB
from ..core.config import mongo_db

def get_mongo_manager() -> MongoDB:
    return mongo_db

# def get_oauth2_scheme(request: Request):
#     oauth2_scheme = request.app.state.oauth2_scheme
#     return oauth2_scheme

# def get_user_service(db: Annotated[Any, Depends(get_mongo_manager)]):
#     return UserService(db)

# def get_authentication_service(db: Annotated[Any, Depends(get_mongo_manager)]):
#     return AuthenticationService(db)