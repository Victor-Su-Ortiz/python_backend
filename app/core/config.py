from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    # App information
    APP_NAME: str = os.getenv("APP_NAME", "Task Management API")
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

    # Security settings
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
