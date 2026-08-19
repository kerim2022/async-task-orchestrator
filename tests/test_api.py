"""Integration tests for FastAPI endpoints."""

import pytest
from httpx import AsyncClient, ASGITransport
from src.api.main import app


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_create_and_get_task():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create Task
        payload = {"payload": "sample transaction data"}
        create_res = await client.post("/tasks/", json=payload)
        assert create_res.status_code == 202
        data = create_res.json()
        assert "task_id" in data
        assert data["status"] == "PENDING"

        task_id = data["task_id"]

        # Fetch Task Status
        get_res = await client.get(f"/tasks/{task_id}")
        assert get_res.status_code == 200
        get_data = get_res.json()
        assert get_data["task_id"] == task_id
        assert get_data["payload"] == "sample transaction data"