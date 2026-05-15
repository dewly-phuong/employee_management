from fastapi import HTTPException, status, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from ..schemas.token import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    CurrentUserResponse,
    TokenData,
)
from ..models.user import User
from ..core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.ACCESS_TOKEN_EXPRIRES_IN_MINUTES)
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
password_hasher = PasswordHash.recommended()


async def login(login_request: LoginRequest) -> LoginResponse:
    """Implementation for login method in IAuthenticationService

    Args:
        login_request (LoginRequest): _description_

    Raises:
        HTTPException: _description_

    Returns:
        LoginResponse: _description_
    """
    logger.info(f"LOGIN SERVICE: ATTEMPTING TO LOGIN USER: {login_request.username}")
    user = await authenticate(login_request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return LoginResponse(access_token=access_token, token_type="bearer")


# Implement register method
async def register(register_request: RegisterRequest) -> bool:
    """Implementation for register method from IAuthenticationService

    Args:
        register_request (RegisterRequest): _description_

    Returns:
        bool: _description_
    """
    logger.info(
        f"REGISTER SERVICE: ATTEMPTING TO REGISTER USER: {register_request.username}"
    )
    return True


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> CurrentUserResponse:
    """Helper method for get_current_user method
        Verify access token and return user information

    Args:
        token (str): _description_
        credentials_exception (HTTPException): _description_

    Raises:
        credentials_exception: _description_
        credentials_exception: _description_

    Returns:
        CurrentUserResponse: _description_
    """
    logger.info("GET CURRENT USER SERVICE: ATTEMPTING TO GET USER")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    logger.info(f"GET CURRENT USER SERVICE: FOUND USER: {token_data.username}")
    user = await User.find_one(User.username == token_data.username)
    if user is None:
        raise credentials_exception
    current_user_response = CurrentUserResponse(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        department=user.department,
        skills=user.skills,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
    return current_user_response


async def authenticate(
    login_request: LoginRequest
) -> User:
    """Helper method for log in method
        Verify user base on username and password

    Args:
        login_request (LoginRequest): _description_

    Returns:
        User: _description_
    """
    logger.info(
        f"AUTHENTICATE SERVICE: ATTEMPTING TO AUTHENTICATE USER: {login_request.username}"
    )
    # employee_collection = db.get_collection("users")
    # user = await employee_collection.find_one({"username": login_request.username})
    # user_model = User()
    user = await User.find_one(User.username == login_request.username)
    if not user:
        return None
    if not verify_password(login_request.password, user.password):
        return None
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """verify password

    Args:
        plain_password (str): password was input by user
        hashed_password (str): password was stored in database
    Returns:
        bool: _description_
    """
    return password_hasher.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """generate hash password from plain password"""
    return password_hasher.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Helper method for log in method
        Create access token for user base on username and password

    Args:
        data (dict): _description_
        expires_delta (timedelta | None, optional): _description_. Defaults to None.

    Returns:
        str: _description_
    """
    logger.info(
        f"CREATE ACCESS TOKEN SERVICE: ATTEMPTING TO CREATE ACCESS TOKEN FOR USER: {data.get('sub')}"
    )
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
