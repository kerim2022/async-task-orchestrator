"""Repository pattern implementation for task persistence."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import TaskRecord, TaskStatus


class TaskRepository:
    """Provides abstracted persistence access for task records."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_task(self, task_id: str, payload: str) -> TaskRecord:
        record = TaskRecord(id=task_id, payload=payload, status=TaskStatus.PENDING)
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def get_by_id(self, task_id: str) -> TaskRecord | None:
        stmt = select(TaskRecord).where(TaskRecord.id == task_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_status(
        self, task_id: str, status: TaskStatus, result_data: str | None = None
    ) -> TaskRecord | None:
        record = await self.get_by_id(task_id)
        if record:
            record.status = status
            if result_data is not None:
                record.result = result_data
            await self.session.commit()
            await self.session.refresh(record)
        return record