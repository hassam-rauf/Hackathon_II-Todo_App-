# Database & SQLModel Patterns Reference

## Neon PostgreSQL Connection

### Connection String Format
```
postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
```

### Engine Setup
```python
import os
from sqlmodel import create_engine, Session

DATABASE_URL = os.getenv("DATABASE_URL")

# Neon requires SSL; connection pooling recommended
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,       # detect stale connections
    pool_size=5,               # default pool
    max_overflow=10,           # burst capacity
)
```

### Session Dependency (FastAPI)
```python
from sqlmodel import Session
from fastapi import Depends

def get_session():
    with Session(engine) as session:
        yield session

# Usage in routes
async def create_task(session: Session = Depends(get_session)):
    ...
```

## SQLModel Patterns

### Model with Relationships
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Read/Create Models (API Layer)
```python
# Base — shared fields
class TaskBase(SQLModel):
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)

# Create — what the client sends
class TaskCreate(TaskBase):
    pass

# Update — all fields optional
class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None

# Table — the database row
class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Response — what the client gets back
class TaskResponse(TaskBase):
    id: int
    completed: bool
    created_at: datetime
```

## Query Patterns

### CRUD Operations
```python
from sqlmodel import select

# CREATE
task = Task(user_id=user_id, title=body.title, description=body.description)
session.add(task)
session.commit()
session.refresh(task)

# READ (single)
task = session.get(Task, task_id)

# READ (list with filter)
stmt = select(Task).where(Task.user_id == user_id)
tasks = session.exec(stmt).all()

# UPDATE (partial)
task = session.get(Task, task_id)
for key, value in update_data.items():
    if value is not None:
        setattr(task, key, value)
task.updated_at = datetime.utcnow()
session.add(task)
session.commit()
session.refresh(task)

# DELETE
task = session.get(Task, task_id)
session.delete(task)
session.commit()
```

### Filtering and Sorting
```python
# Multiple conditions
stmt = select(Task).where(
    Task.user_id == user_id,
    Task.completed == False,
)

# Order by
stmt = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())

# Count
from sqlmodel import func
stmt = select(func.count()).where(Task.user_id == user_id)
count = session.exec(stmt).one()
```

## Alembic Migration Workflow

### Initial Setup
```bash
# Install
uv add alembic

# Initialize
alembic init alembic
```

### Configure alembic/env.py
```python
# Add at top of env.py
from sqlmodel import SQLModel
from src.models import Task  # import all models

# Replace target_metadata line
target_metadata = SQLModel.metadata

# In run_migrations_online(), use DATABASE_URL from env
import os
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))
```

### Migration Commands
```bash
# Generate migration from model changes
alembic revision --autogenerate -m "create tasks table"

# Apply migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1

# Show current revision
alembic current

# Show migration history
alembic history
```

## Neon-Specific Gotchas

| Issue | Solution |
|-------|----------|
| SSL required | Always include `?sslmode=require` in URL |
| Cold starts | Use `pool_pre_ping=True` on engine |
| Connection limits (free tier) | Keep `pool_size` ≤ 5 |
| Branching for dev | Use Neon branch for dev DB, main for prod |
| Schema changes | Always use Alembic, never `create_all()` in prod |

## Testing with SQLite (Local)
```python
import pytest
from sqlmodel import create_engine, Session, SQLModel

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
```
