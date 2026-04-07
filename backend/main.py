"""FastAPI application entry point.

Ref: specs/phase2-web/task-crud/plan.md — App Entry
Task: T-014
"""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db import init_db
from backend.routes.tasks import router as tasks_router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables on startup."""
    init_db()
    yield


app = FastAPI(
    title="Todo API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — T-022
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(tasks_router)


@app.get("/health")
def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}
