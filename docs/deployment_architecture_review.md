# FleetSync — Sprint 2 Deployment Architecture Review

| Field | Value |
|---|---|
| Phase | Sprint 2 — Requirements & Architecture |
| Review author | Deniz Alp Oniki — DevOps & CI/CD Infrastructure Engineer |
| Architecture owner / reviewer | Ali Eren Kurt — Lead Architect |
| Date | 2026-11-21 |
| Tracking | [Issue #282](https://github.com/denizalponiki/Fleet-Tracking-System/issues/282); [Architecture issue #237](https://github.com/denizalponiki/Fleet-Tracking-System/issues/237) |
| Status | **Proposed findings — pending architecture/team sign-off** |

## Review scope and sources

This is a **design and documentation review**, not a claim that deployment, TLS, CI, database backup, or restoration has been implemented.

- [UML deployment diagram](uml/deployment_diagram.md) — desired topology and DD-1 through DD-4
- [Operational and QA NFRs](nfr_quality_measures.md) — NFR-OPS-01 through OPS-08, especially OPS-02, OPS-04 and OPS-08
- [Docker Compose](../docker-compose.yml) — currently only PostgreSQL with a named `postgres_data` volume
- [Environment example](../.env.example) — currently PostgreSQL values only
- [Backend settings](../backend/app/shared/config.py) — `jwt_secret` required without a default; `database_url` configurable
- [Sprint 2 report](sprint-reports/sprint-2.md) — Sprint 2 deliverables and separation from Sprint 3 implementation

## Deployment decision review

| ID | Finding / current state | Sprint 2 action | Owner and status |
|---|---|---|---|
| **DD-1** | Diagram proposes `web` (Nginx), `api` (FastAPI) and `db` (PostgreSQL) on one Docker Compose host. Current `docker-compose.yml` contains **only** `db`. The named network, readiness checks and web/API services depicted are target-state design, not active infrastructure. | Confirm the topology as the target architecture and preserve the Sprint 3 implementation boundary (US-46). Do not add app containers in Sprint 2. | DevOps + Architect — architecture confirmation pending; implementation Sprint 3 |
| **DD-2** | Diagram depicts local HTTP at `http://localhost:8080` and HTTPS `:443` when configured; team transport decision remains open. | Proposed rule for review: localhost-only demo with synthetic data may use HTTP; anything externally exposed should use HTTPS with a valid certificate. **Do not mark this accepted until the team/architect decides.** | Team / Architect / DevOps — **decision pending** |
| **DD-3** | The backend settings use a required `JWT_SECRET` value (Pydantic `jwt_secret`, no default), but the current `.env.example` contains only PostgreSQL variables. The diagram already names `JWT_SECRET`. | Confirm the exact `JWT_SECRET` and `DATABASE_URL` setting names with backend owner. Document that `.env.example` needs non-secret placeholders, real `.env` files must remain ignored, and no actual credentials belong in Git. Avoid modifying runtime configuration as part of this review. | DevOps + Architect / Backend — **configuration alignment pending** |
| **DD-4** | NFR-OPS-04 already states logical backup with `pg_dump`, storage outside the DB container/volume and verification of restore into a clean DB. No backup/restore execution evidence is present in this review. | Link the requirement to the deployment design; record backup and restore procedure/verification as future implementation or final-demo readiness, not Sprint 2 completed operations. | DevOps + QA — **design described; execution pending** |

## Consistency checks

1. **Single-entry routing:** The proposed Nginx `/api/v1` reverse proxy to internal `api:8000` agrees with NFR-OPS-01 and the deployment diagram. Confirm the chosen web/API network architecture before Sprint 3.
2. **Database isolation:** No host-published PostgreSQL port in the current Compose file, consistent with NFR-OPS-03. Persisting the named `postgres_data` volume is specified; no restoration exercise has been verified yet.
3. **Environment and secrets:** The backend cannot obtain `JWT_SECRET` from the documented `.env.example` alone. This is a configuration documentation gap, **not** authorization to commit a secret.
4. **CI and images:** The deployment diagram's tests/build pipeline is future-state. The current repository workflow includes OpenAPI lint; Sprint 3 implementation gates should not be reported as already running.

## Review questions for Ali Eren and the team

- **DD-1:** Is the one-host Nginx/FastAPI/PostgreSQL diagram the approved target for US-46 in Sprint 3?
- **DD-2:** Has the team decided localhost HTTP versus HTTPS for the actual demo environment? Record the decision with owner and rationale.
- **DD-3:** Can the backend owner confirm `JWT_SECRET` and `DATABASE_URL` naming, and add safe placeholders during the appropriate configuration work?
- **DD-4:** Does NFR-OPS-04 adequately specify backup and restore acceptance evidence for the planned demo?

## Sprint 2 completion criterion

The design review is complete when the architecture owner records feedback/approval and the open decisions are either agreed or explicitly tracked with an owner. **Do not treat a review approval as proof of Sprint 3 deployment implementation.**
