# Plann.er - AGENTS.md

## Project Overview
Python FastAPI application with Clean Architecture for trip planning. Uses async SQLAlchemy, PostgreSQL, Alembic migrations, pytest.

## Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests (unit only, no DB required)
pytest

# Run specific test file
pytest tests/application/use_cases/test_create_trip_use_case.py

# Run with coverage
pytest --cov=app

# Run alembic migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# Start dev server (requires PostgreSQL)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Architecture
```
app/
├── domain/              # Core business logic (entities, value objects, exceptions, ports)
├── application/         # Use cases, DTOs
├── adapters/
│   ├── inbound/         # API layer (FastAPI routes, schemas)
│   └── outbound/        # Database (SQLAlchemy models, repositories, mappers), email
└── infrastructure/      # Config, database engine, unit of work
```

Key patterns:
- **Dependency Injection**: FastAPI deps for DB sessions (`app/adapters/inbound/api/deps.py`)
- **Unit of Work**: `SqlAlchemyUnitOfWork` wraps async session with commit/rollback
- **Repository Pattern**: Domain ports define interfaces, SQLAlchemy implementations in adapters
- **Mappers**: Convert between domain entities and DB models

## Testing
- **Fixtures** (`tests/conftest.py`): `engine` (session), `setup_database` (auto-create/drop), `db_session` (function-scoped with rollback), `client` (httpx AsyncClient)
- **No real DB needed** for unit tests - they mock repositories/UoW
- **Async tests**: Use `@pytest.mark.asyncio` and `AsyncMock`
- **Run single test**: `pytest tests/application/use_cases/test_create_trip_use_case.py::test_create_trip_success`

## Database
- **Dev**: `postgresql+asyncpg://postgres:postgres@db:5432/planner` (from `.env`)
- **Test**: Uses same DATABASE_URL in conftest (should use TEST_DATABASE_URL but currently doesn't)
- **Migrations**: `alembic/` with `env.py` using settings.DATABASE_URL
- **Models**: `app/adapters/outbound/database/models/` - SQLAlchemy declarative models

## Environment
Required `.env` variables:
```
APP_HOST=localhost
APP_PORT=8000
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/planner
TEST_DATABASE_URL=postgresql+asyncpg://postgres:postgres@db-test:5433/planner_test
API_PREFIX=/api
OWNER_NAME=...
EMAIL_USERNAME=...
EMAIL_PASSWORD=...
```

## DevContainer
- `.devcontainer/docker-compose.yml`: Runs `app`, `db` (5432), `db-test` (5433)
- `forwardPorts`: 5432, 5433 in devcontainer.json
- Start: Open in VS Code Dev Containers or `docker compose -f .devcontainer/docker-compose.yml up -d`

## Gotchas
1. **TEST_DATABASE_URL not used** - conftest.py reads `settings.DATABASE_URL` instead of `TEST_DATABASE_URL`
2. **email-validator required** - pydantic email validation needs `pip install email-validator` (not in requirements.txt)
3. **No lint/typecheck configured** - no ruff, mypy, or black in project
4. **Dev DB credentials hardcoded** in docker-compose.yml (postgres/postgres)
5. **No CI/CD pipeline** - only dependabot for devcontainers