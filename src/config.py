"""Application settings and environment configuration."""

import os
from pydantic import BaseModel


class Settings(BaseModel):
    PROJECT_NAME: str = "Async Task Orchestrator"
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./orchestrator.db")


settings = Settings()