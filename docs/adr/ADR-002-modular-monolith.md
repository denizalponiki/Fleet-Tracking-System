# ADR-002: Modular monolith with enforced module boundaries

- Status: Accepted
- Date: 2026-11-21
- Decider: Ali Eren Kurt (Lead Software Architect)
- Consulted: module owners (see `docs/raci_matrix.md`)

## Context

ADR-001 chose one FastAPI backend organised as a modular monolith. Eight modules
(identity, vehicle, maintenance, reservation, carpool, handover, fuel, reporting) are
owned by six different people and written in parallel in Sprint 3. Without explicit
rules the modules would import each other's ORM models and repositories, which makes
ownership unclear, creates import cycles and lets one person's change break another
module. Some flows also cross modules inside one transaction: a vehicle return
(handover) must update the odometer (vehicle), complete the reservation (reservation)
and run the rule engine (maintenance), and either all of it is saved or none of it.

## Decision

1. **One module per bounded context**, as listed in `docs/system_vision.md` §7.1 and
   drawn in `docs/c4/README.md` §3. Each module lives in `backend/app/modules/<name>/`
   with the same files: `api.py`, `router.py`, `schemas.py`, `service.py`, `domain.py`,
   `repository.py`, `models.py`, `events.py`.
2. **Public facade only.** Another module may import only `<module>/api.py`. Models,
   repositories and services are private to their module.
3. **Acyclic dependencies.** The allowed direction is
   `reservation → identity, vehicle, maintenance`; `carpool → reservation`;
   `handover → reservation, vehicle`; `maintenance → vehicle`; `fuel → vehicle, reservation`.
   `reporting` reads only. When a lower module must react to a higher one, it subscribes
   to a **domain event** instead of being called (e.g. `handover` publishes
   `TripCompletedEvent`, `maintenance` consumes it).
4. **Synchronous in-process events.** The event bus in `app/shared/events.py` calls the
   handlers immediately, inside the caller's database transaction. There is no broker
   and no retry queue.
5. **One unit of work per HTTP request.** The SQLAlchemy session is opened by a FastAPI
   dependency and committed once at the end; modules do not commit on their own.
6. **Tables belong to modules.** Only the owning module writes to its tables
   (`docs/uml/er_diagram.md` §3). `reporting` may read through SQL views.
7. **Enforced in CI.** `import-linter` contracts check rules 2 and 3 on every pull request.

## Alternatives considered

| Option | Why not |
|---|---|
| Layered monolith (one `models/`, one `services/` for everything) | No ownership per module; every change touches shared files and causes merge conflicts for seven people |
| Microservices (one service per module) | Distributed transactions for the return flow, seven deployables, network failures; rejected in ADR-001 |
| Asynchronous events with a broker (RabbitMQ, Redis) | The return must report the generated alerts in the same response (`ReturnResult.maintenanceAlerts`); eventual consistency would break that and add an extra container |

## Consequences

- Positive: each owner works in their own folder; reviews map to `CODEOWNERS`; a module
  can later be extracted into a service because its boundary is already an interface.
- Positive: the whole return flow is atomic, as `openapi.yaml` `recordReturn` requires.
- Negative: synchronous handlers make the request slower if a handler is heavy. The rule
  engine evaluates a handful of rules per vehicle, so this is acceptable for release 1.
- Negative: facades add some boilerplate (DTOs between modules instead of ORM objects).
- Follow-up: add the `import-linter` configuration with the repository skeleton (Sprint 3).

## Related

- ADR-001 (Python and FastAPI)
- `docs/c4/README.md` §3 (component diagram and dependency rules)
- `docs/uml/sequence_diagrams.md` SD-6 (return and rule engine in one transaction)
- Issue #242
