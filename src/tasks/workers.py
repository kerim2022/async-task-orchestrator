"""Celery worker task definitions."""

import time
from src.tasks.celery_app import celery_app


@celery_app.task(name="process_batch_data")
def process_batch_data(payload: str) -> str:
    """Background task simulating batch computational work."""
    time.sleep(2)  # Simulate non-blocking asynchronous processing
    transformed = payload.upper()
    return f"Processed: {transformed}"