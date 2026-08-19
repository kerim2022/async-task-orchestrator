"""Application entrypoint and lifecycle events."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api.routes import router
from src.database.connection import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database tables
    await init_db()
    yield


app = FastAPI(
    title="Async Task Orchestrator API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}