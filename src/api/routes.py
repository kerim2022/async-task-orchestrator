"""REST API endpoint definitions."""

import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import TaskCreateRequest, TaskResponse
from src.database.connection import get_db_session
from src.database.repository import TaskRepository
from src.tasks.workers import process_batch_data

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_202_ACCEPTED)
async def dispatch_task(
    request: TaskCreateRequest,
    db: AsyncSession = Depends(get_db_session),
):
    """Enqueues background batch processing job and stores initial state."""
    task_id = str(uuid.uuid4())
    repo = TaskRepository(db)

    task_record = await repo.create_task(task_id=task_id, payload=request.payload)

    # Trigger Celery background task
    try:
        process_batch_data.apply_async(args=[request.payload], task_id=task_id)
    except Exception:
        # Fallback for offline task broker environments
        pass

    return TaskResponse(
        task_id=task_record.id,
        status=task_record.status,
        payload=task_record.payload,
        result=task_record.result,
        created_at=task_record.created_at,
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_status(
    task_id: str,
    db: AsyncSession = Depends(get_db_session),
):
    """Retrieves current processing status and details of an orchestrated task."""
    repo = TaskRepository(db)
    record = await repo.get_by_id(task_id)

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID '{task_id}' not found.",
        )

    return TaskResponse(
        task_id=record.id,
        status=record.status,
        payload=record.payload,
        result=record.result,
        created_at=record.created_at,
    )