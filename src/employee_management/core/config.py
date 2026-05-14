from fastapi.security import OAuth2PasswordBearer
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pwdlib import PasswordHash




class Settings(BaseSettings):
    # Tự động map với biến MONGODB_URL trong .env
    MONGODB_URL: str = Field(alias="MONGODB_URL")
    MONGODB_DBNAME: str = Field(alias="MONGODB_DBNAME")
    
    SECRET_KEY: str = Field(alias="SECRET_KEY")
    ALGORITHM: str = Field(alias="ALGORITHM")
    ACCESS_TOKEN_EXPRIRES_IN_MINUTES: int = Field(alias="ACCESS_TOKEN_EXPRIRES_IN_MINUTES")
    
    # Cấu hình đọc file .env
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    
settings = Settings()
