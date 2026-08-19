# Async Task Orchestrator & Processing Microservice

A production-grade Python microservice architecture built with **FastAPI**, **Celery**, **Redis**, and **SQLAlchemy 2.0 (Async)** using the **Repository Pattern** and **Exponential Backoff** decorator patterns.

## System Architecture

```mermaid
classDiagram
    class TaskRecord {
        +str id
        +str payload
        +TaskStatus status
        +str result
        +datetime created_at
    }

    class TaskRepository {
        -AsyncSession session
        +create_task(task_id: str, payload: str) TaskRecord
        +get_by_id(task_id: str) TaskRecord
        +update_status(task_id: str, status: TaskStatus) TaskRecord
    }

    class TaskCreateRequest {
        +str payload
    }

    class TaskResponse {
        +str task_id
        +TaskStatus status
        +str payload
        +str result
    }

    TaskRepository --> TaskRecord : persists
    TaskResponse --> TaskStatus : uses