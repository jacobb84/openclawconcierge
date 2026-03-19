import os
from datetime import timedelta
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    DATABASE_URL: str = "sqlite:///./concierge.db"
    JWT_SECRET_KEY: str = "jwt-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    API_KEY: str = "default-api-key-change-in-production"
    CORS_ORIGINS: str = "*"
    PLUGINS_DIR: str = "plugins"
    PLUGINS_CONFIG: str = "plugins.yaml"
    
    @property
    def cors_origins_list(self) -> List[str]:
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def jwt_access_token_expires(self) -> timedelta:
        return timedelta(hours=self.JWT_ACCESS_TOKEN_EXPIRE_HOURS)
    
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
