# ADR-001: Python and FastAPI for the backend

- Status: Accepted
- Date: 2026-11-05
- Decider: Ali Eren Kurt (Lead Software Architect)
- Consulted: development team

## Context

FleetSync needs a REST API that follows the API-first contract in `docs/openapi.yaml`.
The team has seven members with mixed experience, and Sprint 3 must deliver a working
MVP. The business rules (maintenance thresholds, reservation conflicts, ride matching)
are deterministic and need no external services.

## Decision

The backend is written in Python 3.12 with FastAPI, SQLAlchemy 2.x and PostgreSQL.
Request and response models are Pydantic classes that match `docs/openapi.yaml`.
The code is a modular monolith: one module per bounded context (identity, vehicle,
maintenance, reservation, carpool, handover, fuel, reporting). Modules talk only through
each module's public `api.py` and in-process domain events.

## Alternatives considered

| Option | Why not |
|---|---|
| Java + Spring Boot | Heavier setup; fewer team members know it; slower to reach a demo |
| Node.js + Express | No built-in request validation or OpenAPI generation |
| Microservices | Too much operational cost for seven people and a 10-week schedule |

## Consequences

- Positive: validation and OpenAPI output come from Pydantic; tests use pytest and
  pytest-cov (CI fails below 50% coverage); the whole stack is open source and
  MIT-compatible.
- Negative: no compile-time type checking, so we rely on type hints, tests and linting.
- Follow-up: an architecture test checks that no module imports another module's
  internals; a CI contract test compares `app.openapi()` with `docs/openapi.yaml`.

## Related

- `docs/problem_definition.md` §7 (technical feasibility)
- `docs/test_plans_and_coverage.md` (test stack)
- Issue #135
