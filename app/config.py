# app/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: Optional[str] = None 
    GEMINI_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()