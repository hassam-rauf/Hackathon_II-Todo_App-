---
name: database-sqlmodel-builder
description: |
  Build SQLModel database models, Neon PostgreSQL connections, and Alembic migrations.
  This skill should be used when users ask to create database models, tables, schemas,
  migrations, queries, or connect to Neon serverless database.
---

# Database SQLModel Builder

Build database layer with SQLModel ORM and Neon PostgreSQL.

## What This Skill Does
- Create SQLModel table models with relationships
- Set up Neon serverless PostgreSQL connection
- Generate Alembic migrations
- Build typed queries (select, filter, join)
- Manage database sessions and connection pooling
- Seed test data

## What This Skill Does NOT Do
- API endpoint creation (use fastapi-backend-builder)
- Frontend data display (use frontend-ui-builder)
- Authentication (use auth-builder)

---

## Before Implementation

| Source | Gather |
|--------|--------|
| **Codebase** | Existing models, db.py, migration history |
| **Conversation** | What entity, fields, relationships, constraints |
| **Skill References** | `references/patterns.md` for model and query patterns |
| **User Guidelines** | Constitution database principles |

---

## Workflow

1. **Define model** — SQLModel class with `table=True`, fields, indexes
2. **Set up connection** — engine with DATABASE_URL from env
3. **Create migration** — `alembic revision --autogenerate`
4. **Write queries** — typed select/filter/join using SQLModel syntax
5. **Test** — model creation, CRUD operations, edge cases

---

## Domain Standards

### Must Follow
- `table=True` on all database models
- `Field(index=True)` on frequently queried columns (user_id, completed)
- `Optional[int] = Field(default=None, primary_key=True)` for auto-increment PKs
- Connection string from `DATABASE_URL` environment variable
- Alembic for all schema changes after initial creation
- `sslmode=require` for Neon connections

### Must Avoid
- Raw SQL strings (use SQLModel select/where)
- `create_all()` in production (use Alembic migrations)
- N+1 queries (use joins or eager loading)
- Missing indexes on foreign keys
- Storing secrets in code (use .env)

---

## Key Patterns

### Model Definition
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Neon Connection
```python
import os
from sqlmodel import create_engine, Session

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session
```

### Alembic Setup
```bash
alembic init alembic
# Edit alembic/env.py: import models, set target_metadata = SQLModel.metadata
# Edit alembic.ini: sqlalchemy.url = (use env var)
alembic revision --autogenerate -m "create tasks table"
alembic upgrade head
```

### Query Patterns
```python
from sqlmodel import select

# Get all user tasks
stmt = select(Task).where(Task.user_id == user_id)
tasks = session.exec(stmt).all()

# Filter by status
stmt = select(Task).where(Task.user_id == user_id, Task.completed == False)

# Get single task
task = session.get(Task, task_id)
```

---

## Output Checklist

- [ ] Model has `table=True` and proper Field definitions
- [ ] Primary key is `Optional[int]` with `default=None`
- [ ] Indexes on user_id and frequently filtered columns
- [ ] DATABASE_URL from environment variable
- [ ] Alembic migration generated (not raw create_all in prod)
- [ ] No raw SQL strings

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/patterns.md` | Model patterns, Neon gotchas, migration workflow |
