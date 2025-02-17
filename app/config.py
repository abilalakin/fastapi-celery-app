import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/pipeline_db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    API_ENDPOINT: str = os.getenv("API_ENDPOINT", "https://jsonplaceholder.typicode.com/todos/1")  # External API endpoint

    class Config:
        env_file = ".env"

settings = Settings()
