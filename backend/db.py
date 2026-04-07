"""Neon PostgreSQL connection and session management.

Ref: specs/phase2-web/task-crud/plan.md — Database Layer
Task: T-013
"""

import os

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
) if DATABASE_URL else None


def get_session():
    """FastAPI dependency — yields a database session."""
    with Session(engine) as session:
        yield session


def init_db() -> None:
    """Create all tables. Used on startup for initial setup."""
    SQLModel.metadata.create_all(engine)
