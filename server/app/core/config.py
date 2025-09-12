"""Configuration settings for the application"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App settings
    app_name: str = "Mini-Uber API"
    version: str = "1.0.0"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # Database settings - these will be loaded from .env
    database_url: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()

# Print config for debugging (remove in production)
if __name__ == "__main__":
    print("Current settings:")
    print(f"Database URL: {settings.database_url}")
    print(f"Debug mode: {settings.debug}")