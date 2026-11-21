# FleetSync · Non-Functional Requirements and Quality Measures

| Field | Value |
|---|---|
| Course / phase | BM 321 / SENG 321 · Sprint 2 — Requirements & Architecture |
| Status | **Draft — operational NFRs for review; QA quality measures pending** |
| Operational requirements owner | Deniz Alp Oniki · DevOps & CI/CD Infrastructure Engineer |
| Quality / test requirements co-owner | Abdullah Tecimen · QA & Test Automation Engineer |
| Architecture approver | Ali Eren Kurt · Lead Software Architect & Technical Lead |
| Related issue | [#246](https://github.com/denizalponiki/Fleet-Tracking-System/issues/246) |
| Related architecture | [Deployment diagram](uml/deployment_diagram.md), [C4 model](c4/README.md) |
| Supporting references | [ADR-001](adr/ADR-001-python-fastapi.md), [CI/CD and reporting](ci_cd_and_cost_reporting_api.md), [Git-Flow](git_flow.md) |

## 1. Purpose and scope

This document defines **testable non-functional requirements** and planned quality measures for FleetSync. Sprint 2 specifies the requirements and verification strategy; it does **not** claim that the planned runtime or CI jobs have already been implemented.

**Current state (verified against Sprint 1 repository):** the root `docker-compose.yml` defines the PostgreSQL 16 `db` service with a named `postgres_data` volume; `.env.example` contains PostgreSQL settings; `.github/workflows/openapi-lint.yml` runs Redocly OpenAPI lint on PRs and pushes to `develop` or `main`. The full frontend/backend Compose stack, automated tests, coverage gates, image builds, monitoring and recovery procedure are **not yet implemented**.

**Target architecture:** a React SPA served by Nginx (`web`), a Python 3.12/FastAPI backend (`api`), PostgreSQL 16 (`db`), and persistent DB storage. `web` forwards `/api/v1` to `api`; the database is only accessible to internal services. See the deployment diagram for the proposed ports and dependencies. The implementation target for the full stack is Sprint 3 (US-46).

### 1.1 Requirement conventions

Each requirement uses: **ID**, **statement**, **measurable pass criteria**, **verification evidence**, **target delivery**. Numerical values below are **team-proposed acceptance targets**, not requirements quoted from the course rubric, unless explicitly labelled as such. The Product Owner, QA and Architect should approve them before baselining the SRS.

## 2. Operational NFRs — DevOps responsibility

### NFR-OPS-01 · Reproducible one-command deployment

**Statement:** The complete demo application shall be startable on a machine with Docker Engine and Docker Compose installed using one documented command, `docker compose up --build`, after providing documented configuration.

**Pass criteria:** The `web`, `api` and `db` services start without manual per-service installation; the browser can load the web application; the API endpoint is reachable via the web reverse proxy; the API can communicate with the database. A clean-start procedure and prerequisites are documented.

**Verification:** On a clean machine, copy `.env.example` to `.env`, supply non-default local secrets, run `docker compose up --build`, and record service health, API response, and screenshots/logs. **Target:** Sprint 3 / US-46. **Sprint 2 evidence:** architecture, requirement and verification plan only.

### NFR-OPS-02 · Configuration and secret isolation

**Statement:** Environment-dependent settings and secrets shall be externalized rather than hard-coded in source, Docker images, or committed environment files.

**Pass criteria:** `.env.example` contains variable names and non-secret examples; real `.env` files and credentials are Git-ignored; `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, database URL/configuration and `JWT_SECRET` are configurable. The application fails clearly if required settings are absent. Secrets must not be written to normal application logs.

**Verification:** Inspect source, Compose configuration and `.gitignore`; start with missing required settings and confirm an explicit startup error; check that actual secrets are absent from tracked files. **Target:** Sprint 3. **Open decision:** Deployment diagram DD-3 (`JWT_SECRET` example) — update `.env.example` when API configuration is implemented.

### NFR-OPS-03 · Database persistence and isolation

**Statement:** PostgreSQL data shall persist across service restarts and normal container recreation, and shall not be reachable directly from outside the Compose network in the demo release.

**Pass criteria:** PostgreSQL data uses the named `postgres_data` volume; a test record survives `docker compose down` followed by `docker compose up` (without `-v`); DB port 5432 is not published on the host in the target stack; the backend connects to the `db` service over the internal network.

**Verification:** Write/read a test row before and after service recreation; inspect `docker compose config` and published ports. **Target:** Sprint 3. **Current:** `postgres_data` volume is already declared, but end-to-end persistence has not been verified.

### NFR-OPS-04 · Database backup and restoration

**Statement:** A repeatable PostgreSQL backup and restore procedure shall be documented and validated before the final demonstration.

**Proposed pass criteria:** A backup can be generated using `pg_dump`, stored **outside** the database container and its data volume, and restored to a clean database with core sample records intact. A restore verification log must record the backup file name, timestamp, test and outcome. No real secrets or personal data are stored in the repository.

**Verification:** Create sample records, produce a logical backup, restore it into a disposable fresh database, and compare selected counts and records. Document that `docker compose down -v` deletes the named volume and should not be used in routine restart or recovery. **Target:** Final demo readiness; procedure designed in Sprint 2. **Open decision:** Deployment diagram DD-4.

### NFR-OPS-05 · Recovery and service readiness

**Statement:** Transient container restarts shall not require manual database reconfiguration and application readiness shall be distinguishable from process start.

**Proposed pass criteria:** PostgreSQL health is checked using `pg_isready`; the API waits for database readiness before migrations or queries; a documented recovery test restarts `api` and `db` and confirms that the application can resume access to existing data. The application exposes a simple readiness endpoint or equivalent verifiable check.

**Verification:** Start with the database unavailable, then recover it; inspect Compose health status and test application response; preserve logs of the recovery test. **Target:** Sprint 3 implementation and Final verification.

### NFR-OPS-06 · Automated pull request quality gates

**Statement:** All pull requests targeting `develop` shall run automated checks relevant to the changed application and API contract before merge.

**Pass criteria:** OpenAPI lint remains enabled; Sprint 3 adds backend tests, frontend checks/build, and published backend coverage. The QA target of **at least 50% unit-test coverage** comes directly from the course specification. Backend CI fails when verified total coverage falls below 50%. Protected branches require the team's documented review and passing checks.

**Verification:** Inspect GitHub Actions runs for a sample PR; deliberately introduce an invalid OpenAPI contract or failing test in a temporary branch and confirm a failed check; confirm a successful PR is green before merge. **Target:** Sprint 3 / US-48 and US-49 (QA co-owner). **Current:** only OpenAPI lint exists.

### NFR-OPS-07 · Deployment documentation and observability

**Statement:** The team shall be able to diagnose service failure and reproduce the demo environment from repository documentation.

**Proposed pass criteria:** README or deployment instructions specify prerequisites, local URLs, config variables, startup and shutdown commands, health/status checks, log inspection, backup/restore steps and common failure recovery. Relevant service logs can be viewed through `docker compose logs`; logs should identify failures without leaking credentials or JWTs.

**Verification:** A team member not responsible for the deployment follows the written setup procedure and records whether each step succeeds. **Target:** Sprint 3 / Final.

### NFR-OPS-08 · Local transport and exposure decision

**Statement:** The demo shall use a documented network exposure and transport model appropriate to its environment.

**Proposed decision:** For **localhost-only** development and jury demonstration, HTTP on `http://localhost:8080` may be used if the demo does not transmit real personal data. Any **publicly exposed** environment must use HTTPS with a valid certificate, with the API kept behind the reverse proxy and database port unexposed.

**Verification:** Confirm base URL, exposed ports and HTTPS configuration against the chosen demo environment and updated deployment diagram. **Target:** Architecture decision during Sprint 2; deployment implementation in Sprint 3. **Open decision:** Deployment diagram DD-2 — Ali Eren Kurt to confirm before marking this NFR approved.

## 3. Operational traceability

| NFR | Architecture / implementation evidence | Backlog link | Review |
|---|---|---|---|
| OPS-01 | `docker-compose.yml`, deployment diagram | US-46 | DevOps + Architect |
| OPS-02 | `.env.example`, `.gitignore`, backend settings | US-46 | DevOps + Architect |
| OPS-03 | `docker-compose.yml`, `postgres_data` | US-46 | DevOps |
| OPS-04 | Documented `pg_dump` restore exercise | Final readiness | DevOps + QA |
| OPS-05 | Service health checks and restart test | US-46 | DevOps + QA |
| OPS-06 | `.github/workflows/`, test/coverage report | US-48, US-49 | DevOps + QA |
| OPS-07 | README / deployment runbook | US-46 | DevOps |
| OPS-08 | C4 and UML deployment diagram, deployment config | DD-2 | DevOps + Architect |

## 4. QA / product quality requirements — pending co-author review

**Owner: Abdullah Tecimen (QA & Test Automation Engineer).** The Sprint 2 shared deliverable also requires measurable performance, security, accessibility, reliability and test-quality targets. These sections remain **TBD** until QA/PO agreement; they must **not** be interpreted as complete requirements merely because the operational section is drafted.

- **Performance:** Agree tested endpoints, concurrent-user/load assumptions, response-time percentile and measurement tooling.
- **Security:** Agree authentication, authorization, invalid JWT behavior, input validation and secret-handling test evidence; maintain the existing requirement that `STAFF` cannot access fleet reports.
- **Accessibility / usability:** Agree the UI accessibility baseline and how it will be tested against Figma and the later app.
- **Testing:** Agree unit, integration and end-to-end test scope; course minimum is **50% unit-test coverage**.
- **Consistency / availability:** Agree reservation conflict tests and measurable recovery/readiness evidence.

## 5. Sprint 2 review and open decisions

| Item | Requested owner | Status |
|---|---|---|
| Review operational acceptance targets for feasibility | Ali Eren Kurt | Open |
| Approve localhost HTTP vs public HTTPS rule (DD-2) | Ali Eren Kurt + Deniz Alp Oniki | Open |
| Confirm API/JWT environment-variable names (DD-3) | Ali Eren Kurt + Deniz Alp Oniki | Open |
| Review backup/restore method (DD-4) | Deniz Alp Oniki + Abdullah Tecimen | Open |
| Add and baseline measurable QA metrics | Abdullah Tecimen | Open |
| Reconcile with SRS and traceability | Ahmet Can Vurmaz | Open |

**Sprint 2 exit condition:** Requirement IDs, measurable acceptance criteria and verification methods are documented and reviewed. Do not mark future operational implementation as complete until its tests have actually run.
