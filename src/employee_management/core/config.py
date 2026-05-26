from fastapi.security import OAuth2PasswordBearer
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Settings(BaseSettings):
    # Tự động map với biến MONGODB_URL trong .env
    MONGODB_URL: str = Field(alias="MONGODB_URL")
    MONGODB_DBNAME: str = Field(alias="MONGODB_DBNAME")
    
    SECRET_KEY: str = Field(alias="SECRET_KEY")
    ALGORITHM: str = Field(alias="ALGORITHM")
    ACCESS_TOKEN_EXPRIRES_IN_MINUTES: int = Field(alias="ACCESS_TOKEN_EXPRIRES_IN_MINUTES")
    
    # Cấu hình đọc file .env
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"), env_file_encoding="utf-8", extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

