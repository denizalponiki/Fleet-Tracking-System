# FleetSync backend

Python 3.12 · FastAPI · SQLAlchemy 2.x · PostgreSQL 16. Architecture: [ADR-001](../docs/adr/ADR-001-python-fastapi.md), [ADR-002](../docs/adr/ADR-002-modular-monolith.md), [C4 Level 3](../docs/c4/README.md#3-level-3--components-of-the-backend-api).

## Layout

```text
backend/
├── pyproject.toml          # dependencies, pytest/coverage (>= 50%), ruff, import-linter contracts
├── app/
│   ├── main.py             # create_app(): mounts every module router under /api/v1, GET /api/v1/health
│   ├── shared/             # config, db (unit of work), problems (RFC 9457), security (JWT, roles), events
│   └── modules/
│       └── <module>/       # identity, vehicle, maintenance, reservation, carpool, handover, fuel, reporting
│           ├── api.py          # public facade: the ONLY file other modules may import
│           ├── router.py       # FastAPI routes = operations of this module's OpenAPI tags
│           ├── schemas.py      # Pydantic models matching docs/openapi.yaml
│           ├── service.py      # use cases (no commit; the request commits once)
│           ├── domain.py       # rules; raise DomainError(status, code, detail)
│           ├── repository.py   # queries on this module's tables
│           ├── models.py       # ORM tables (docs/uml/er_diagram.md), private
│           └── events.py       # events published / handlers subscribed
└── tests/
```

## Run locally

Requires [uv](https://docs.astral.sh/uv/). From `backend/`:

```bash
uv sync
```

```bash
uv run pytest
```

```bash
uv run lint-imports
```

```bash
uv run uvicorn app.main:app --reload --port 8000
```

`JWT_SECRET` must be set (in `.env` or the environment); `DATABASE_URL` defaults to the local `db` settings from `.env.example`.

## Rules for module owners

1. Work only inside your module folder; add one route per operation of your OpenAPI tag, with the same `operationId`.
2. Need another module? Call its `api.py`. If the function you need is missing, ask its owner to add it there.
3. Need to react to another module? Subscribe to its event in your `events.py` (example: `maintenance` handles `TripCompleted` from `handover`).
4. Errors: `raise DomainError(409, "RESERVATION_CONFLICT", "...")` with a code from `ErrorCode` in `openapi.yaml`.
5. Roles: `Depends(require_role(Role.FLEET_MANAGER))` or `Depends(current_user)`.

`uv run pytest` fails if a module imports another module's internals; `uv run lint-imports` fails if a dependency goes the wrong way.
