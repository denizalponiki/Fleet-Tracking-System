# FleetSync — Sprint 2 Deployment Architecture Review

| Field | Value |
|---|---|
| Phase | Sprint 2 — Requirements & Architecture |
| Review author | Deniz Alp Oniki — DevOps & CI/CD Infrastructure Engineer |
| Architecture owner / reviewer | Ali Eren Kurt — Lead Architect |
| Date | 2026-11-21 |
| Tracking | [Issue #282](https://github.com/denizalponiki/Fleet-Tracking-System/issues/282); [Architecture issue #237](https://github.com/denizalponiki/Fleet-Tracking-System/issues/237) |
| Status | **Review updated 2026-11-23 — DD-2/DD-3 decisions confirmed; DD-1 implementation and DD-4 verification remain pending** |

## Review scope and sources

This is a **design and documentation review**, not a claim that deployment, TLS, CI, database backup, or restoration has been implemented.

- [UML deployment diagram](uml/deployment_diagram.md) — desired topology and DD-1 through DD-4
- [Operational and QA NFRs](nfr_quality_measures.md) — NFR-OPS-01 through OPS-08, especially OPS-02, OPS-04 and OPS-08
- [DD-4 backup/restore verification design](backup_restore_design.md) — proposed logical backup and isolated restore evidence plan (not executed)
- [Docker Compose](../docker-compose.yml) — currently only PostgreSQL with a named `postgres_data` volume
- [Environment example](../.env.example) — currently PostgreSQL values only
- [Backend settings](../backend/app/shared/config.py) — `jwt_secret` required without a default; `database_url` configurable
- [Sprint 2 report](sprint-reports/sprint-2.md) — Sprint 2 deliverables and separation from Sprint 3 implementation

## Deployment decision review

| ID | Finding / current state | Sprint 2 action | Owner and status |
|---|---|---|---|
| **DD-1** | Diagram proposes `web` (Nginx), `api` (FastAPI) and `db` (PostgreSQL) on one Docker Compose host. Current `docker-compose.yml` contains **only** `db`. The named network, readiness checks and web/API services depicted are target-state design, not active infrastructure. | Confirm the topology as the target architecture and preserve the Sprint 3 implementation boundary (US-46). Do not add app containers in Sprint 2. | DevOps + Architect — architecture confirmation pending; implementation Sprint 3 |
| **DD-2** | The deployment diagram distinguishes localhost HTTP from HTTPS for public exposure. | Decision recorded in NFR-OPS-08: localhost-only demo with synthetic data uses HTTP at `http://localhost:8080`; any publicly exposed deployment requires HTTPS with a valid certificate, keeping the API behind the reverse proxy and DB port unexposed. This is an approved design decision, **not evidence of an implemented web service or HTTPS deployment**. | Architect + DevOps — **architecture decision approved; implementation Sprint 3** |
| **DD-3** | `backend/app/shared/config.py` uses `DATABASE_URL` (configurable) and requires `JWT_SECRET`; the current `.env.example` still lists only PostgreSQL variables. | NFR-OPS-02 records the Architect's confirmed names: `DATABASE_URL`, `JWT_SECRET`, `JWT_EXPIRES_SECONDS` (default 3600), plus default `JWT_ALGORITHM` (HS256) and `JWT_ISSUER` (fleetsync). The non-secret placeholders and Compose API wiring are **planned with DD-1 in Sprint 3**, not present in the current repo. No secrets are committed. | Architect + DevOps — **names confirmed; `.env.example` / Compose changes pending Sprint 3** |
| **DD-4** | NFR-OPS-04 requires a logical backup with `pg_dump`, archive storage outside the DB container/volume and restore verification against an empty database. No restore execution evidence is available. | [Backup/restore verification design](backup_restore_design.md) specifies the proposed archive, isolated restore, record comparison and evidence fields; final verification still requires execution and QA review. | DevOps + QA — **design specified for review; restore untested** |

## Consistency checks

1. **Single-entry routing:** The proposed Nginx `/api/v1` reverse proxy to internal `api:8000` agrees with NFR-OPS-01 and the deployment diagram. Confirm the chosen web/API network architecture before Sprint 3.
2. **Database isolation:** No host-published PostgreSQL port in the current Compose file, consistent with NFR-OPS-03. Persisting the named `postgres_data` volume is specified; no restoration exercise has been verified yet.
3. **Environment and secrets:** The backend cannot obtain `JWT_SECRET` from the documented `.env.example` alone. This is a configuration documentation gap, **not** authorization to commit a secret.
4. **CI and images:** The deployment diagram's tests/build pipeline is future-state. The current repository workflow includes OpenAPI lint; Sprint 3 implementation gates should not be reported as already running.

## Review questions for Ali Eren and the team

- **DD-1:** Is the one-host Nginx/FastAPI/PostgreSQL diagram the approved target for US-46 in Sprint 3?
- **DD-2:** Decision already recorded in NFR-OPS-08: localhost HTTP for the synthetic local demo; HTTPS with a valid certificate if publicly exposed. Verify the implemented environment against this decision during Sprint 3.
- **DD-3:** Environment-variable names are confirmed in NFR-OPS-02; verify that Sprint 3's DD-1 Compose/API changes introduce safe `.env.example` placeholders and do not commit real secrets.
- **DD-4:** Does NFR-OPS-04 adequately specify backup and restore acceptance evidence for the planned demo?

## Sprint 2 completion criterion

The design review is complete when the architecture owner records feedback/approval and the open decisions are either agreed or explicitly tracked with an owner. **Do not treat a review approval as proof of Sprint 3 deployment implementation.**
