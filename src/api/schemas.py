"""Pydantic schemas for request/response serialization."""

from datetime import datetime
from pydantic import BaseModel, Field
from src.database.models import TaskStatus


class TaskCreateRequest(BaseModel):
    payload: str = Field(..., min_length=1, description="Data payload to orchestrate.")


class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    payload: str
    result: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True