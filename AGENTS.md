# Plann.er - AGENTS.md

## Project Overview
Python FastAPI application with Clean Architecture for trip planning. Uses async SQLAlchemy, PostgreSQL, Alembic migrations, pytest.

## Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests (REQUIRES the db-test PostgreSQL to be up, see Testing)
pytest

# Run specific test file
pytest tests/application/use_cases/test_create_trip_use_case.py

# Run with coverage (pytest-cov + coverage are in requirements)
pytest --cov=app

# Apply migrations (run from repo root)
alembic upgrade head

# Create new migration (autogenerate reads app models via alembic/env.py)
alembic revision --autogenerate -m "description"

# Start dev server (requires PostgreSQL + `alembic upgrade head`)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Architecture
```
app/
├── domain/              # Entities, value objects, exceptions, ports
│   └── ports/           # input_ports/ (use case ifaces), output_ports/ (repo, UoW, notification)
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
- **Real entrypoint**: `app.main:app` (app never creates tables itself — schema comes only from Alembic)

## Testing
- `tests/conftest.py` has a **session-scoped autouse** `setup_database` fixture that connects to `TEST_DATABASE_URL` and runs `Base.metadata.create_all` / `drop_all`. So `pytest` needs the `db-test` service running even though the use-case tests are mock-based unit tests.
- Fixtures: `engine` (session), `setup_database` (auto create/drop), `db_session` (function-scoped with rollback), `client` (httpx AsyncClient).
- Async tests use `@pytest.mark.asyncio` (and `asyncio_mode = auto` in `pytest.ini`); repositories/UoW are mocked with `AsyncMock`.
- Run single test: `pytest tests/application/use_cases/test_create_trip_use_case.py::test_create_trip_success`

## Database
- **Dev**: `postgresql+asyncpg://postgres:postgres@db:5432/planner` (from `.env`)
- **Test**: `postgresql+asyncpg://postgres:postgres@db-test:5432/planner_test` (from `.env`)
- **Migrations**: `alembic/` with `env.py` reading `settings.DATABASE_URL`; Alembic swaps `+asyncpg` -> `+psycopg2` (sync driver) for its own engine.
- **Autogenerate**: `alembic/env.py` imports `_all_models`, so new models must be added there to be detected.
- **Models**: `app/adapters/outbound/database/models/` - SQLAlchemy declarative models (shared `id`/`created_at`/`updated_at` in `base.py`).

## Environment
Required `.env` variables:
```
APP_HOST=localhost
APP_PORT=8000
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/planner
TEST_DATABASE_URL=postgresql+asyncpg://postgres:postgres@db-test:5432/planner_test
API_PREFIX=/api
OWNER_NAME=...
EMAIL_USERNAME=...
EMAIL_PASSWORD=...
```

## DevContainer
- `.devcontainer/docker-compose.yml`: runs `app`, `db`, `db-test` on the `planner-network` bridge.
  - Inside the network both DBs are on port 5432 (`db:5432`, `db-test:5432`).
  - Host port mappings: `db` = `5434:5432`, `db-test` = `5433:5432`.
- `forwardPorts`: 5432, 5433 in `devcontainer.json` (note: `db`'s host port is 5434).
- Start: Open in VS Code Dev Containers or `docker compose -f .devcontainer/docker-compose.yml up -d`.

## Gotchas
1. **Tests need the DB** - the autouse `setup_database` fixture connects to `TEST_DATABASE_URL`; `pytest` fails if `db-test` is down.
2. **Tables come only from Alembic** - the app has no `create_all`; running `uvicorn` without `alembic upgrade head` yields missing-table errors.
3. **Alpine `alembic_version` desync** - if `alembic current` reports `ddc9b297ed70 (head)` but actual tables are absent (e.g. an old volume/test run dropped them), `alembic upgrade head` is a no-op. Reset with `alembic stamp base && alembic upgrade head`. (Historically caused by conftest dropping tables on the dev DB; now fixed to use `TEST_DATABASE_URL`.)
4. **Run Alembic from repo root** - `alembic.ini` sets `prepend_sys_path = .` so `app.*` imports resolve.
5. **No lint/typecheck configured** - no ruff, mypy, black, or pre-commit in the project.
6. **Dev DB credentials hardcoded** in `docker-compose.yml` (postgres/postgres).
7. **No CI/CD pipeline** - only `.github/dependabot.yml` for devcontainer updates.
