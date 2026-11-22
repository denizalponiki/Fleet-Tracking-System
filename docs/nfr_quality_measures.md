# FleetSync · Non-Functional Requirements and Quality Measures

| Field | Value |
|---|---|
| Course / phase | BM 321 / SENG 321 · Sprint 2 — Requirements & Architecture |
| Status | **Draft — operational and QA quality NFRs for review** |
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

**Verification:** Inspect source, Compose configuration and `.gitignore`; start with missing required settings and confirm an explicit startup error; check that actual secrets are absent from tracked files. **Target:** Sprint 3. **Decision (DD-3, Architect, 2026-11-21):** the API reads `DATABASE_URL`, `JWT_SECRET` (required, no default; the API does not start without it) and `JWT_EXPIRES_SECONDS` (default `3600`, ADR-005); `JWT_ALGORITHM` (`HS256`) and `JWT_ISSUER` (`fleetsync`) have safe defaults. The `db` service keeps `POSTGRES_DB`, `POSTGRES_USER` and `POSTGRES_PASSWORD`. These are the names used in `backend/app/shared/config.py`. `JWT_SECRET` and `DATABASE_URL` are added to `.env.example` together with the `api` service in Compose (DD-1).

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

**Decision (DD-2, approved by the Architect, 2026-11-21):** For **localhost-only** development and jury demonstration, HTTP on `http://localhost:8080` is used; the demo uses only invented seed data (US-47), so no real personal data is transmitted. Any **publicly exposed** environment must use HTTPS with a valid certificate, with the API kept behind the reverse proxy and database port unexposed. A self-signed certificate for the demo is not used: it adds browser warnings without protecting real data.

**Verification:** Confirm base URL, exposed ports and HTTPS configuration against the chosen demo environment and updated deployment diagram. **Target:** Architecture decision in Sprint 2 (done); deployment implementation in Sprint 3.

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

## 4. QA / product quality NFRs — QA responsibility

**Owner: Abdullah Tecimen (QA & Test Automation Engineer).** This section uses the same format as section 2. All numbers are **team-proposed targets** except the 50% unit-test coverage, which comes from the course specification. They are sized for the expected scale in `system_vision.md` A6 (tens of vehicles, hundreds of users) and for a single-machine Docker Compose demo. Test case IDs refer to [`test_plans_and_coverage.md`](test_plans_and_coverage.md); planned new IDs are marked *(new)* and will be added to the test plan when the tests are written.

### 4.1 Performance

#### NFR-PERF-01 · API response time

**Statement:** Under the expected demo load, the API shall answer typical requests fast enough that the UI feels immediate.

**Pass criteria:** With the full Compose stack and demo seed data (US-47), a load test of **20 concurrent virtual users for 5 minutes** shows:

| Endpoint group | p95 response time | Error rate |
|---|---|---|
| Read endpoints (`GET /vehicles`, `GET /reservations`, `GET /maintenance/alerts`, `GET /locations`, `GET /me`) | ≤ 500 ms | < 1% |
| Write endpoints (`POST /reservations`, `POST /fuel-receipts`, pickup / return) | ≤ 800 ms | < 1% (expected `409`/`422` business errors are not counted as errors) |
| `GET /vehicles/recommendations` | ≤ 1,000 ms | < 1% |
| Reports (`/reports/*`) for one month of seed data | ≤ 2,000 ms | < 1% |

**Verification:** Load test script with **Locust** (Python) in the repository; the report (p50, p95, max, error rate per endpoint) and the machine specification are attached to the test report. The same run is repeated once to show the result is stable. **Target:** Script in Sprint 3 after US-46; measured result for Final.

#### NFR-PERF-02 · Bounded list responses

**Statement:** List endpoints shall not return unbounded result sets.

**Pass criteria:**
- **Paginated lists** (`Page` and `Size` parameters in `openapi.yaml`: `GET /users`, `GET /vehicles`, `GET /reservations`, `GET /maintenance/alerts`) return at most 20 items by default; `size` above 100 is rejected with `400 VALIDATION_ERROR`.
- **Period-bounded lists** (`GET /vehicles/{vehicleId}/fuel-receipts`, `GET /fuel/anomalies`, `GET /expenses`). **Decision (Architect, 2026-11-21, revised 2026-11-22):** these stay unpaginated in release 1 and the **server** bounds them by period, whatever the client sends: without `from` and `to` the server uses the last 92 days up to today (Europe/Istanbul); a period longer than 366 days, or `to` before `from`, is rejected with `400 VALIDATION_ERROR`. This is part of the contract (`openapi.yaml`, parameters `ListFromDate` / `ListToDate`). At the expected scale (`system_vision.md` A6: tens of vehicles) a 366-day period is a few hundred rows at most, within the PERF-01 read target. Adding pagination later would change the response from an array to a page object, a breaking change (`openapi.yaml` 2.0.0); this is accepted for release 1.

**Verification** *(new: TC-NFR-PERF-02)*, **Target:** Sprint 3:
- Paginated lists: request with no parameters → at most 20 items; request with `size=101` → `400 VALIDATION_ERROR`.
- Period-bounded lists (these do not accept `size`): seed data spread over more than a year; request with no `from` / `to` → only items of the last 92 days; `from`/`to` spanning 366 days → `200`; spanning 367 days → `400 VALIDATION_ERROR`; `to` before `from` → `400 VALIDATION_ERROR`.

#### NFR-PERF-03 · Web page load

**Statement:** The main screens of the SPA shall load quickly on a normal campus computer.

**Pass criteria:** Lighthouse (desktop profile) performance score **≥ 80** for the login, trip request and maintenance alerts screens served by the production build behind Nginx; Largest Contentful Paint ≤ 2.5 s.

**Verification:** Lighthouse report for the three screens attached to the Final test report. **Target:** Final.

### 4.2 Security

These requirements turn `system_vision.md` §10 (Security, KVKK) and ADR-005 into testable checks.

#### NFR-SEC-01 · Authentication on every protected operation

**Statement:** Every API operation except `POST /auth/login` shall require a valid JWT.

**Pass criteria:** For **100% of protected operations in `openapi.yaml`**, a request with (a) no token, (b) a malformed token, (c) a token signed with a different secret and (d) an expired token returns `401 UNAUTHORIZED` as `application/problem+json`. Tokens expire after 60 minutes (`expiresIn: 3600`).

**Verification:** A parametrised pytest that reads the operation list from `openapi.yaml` and runs the four cases against each operation, so new endpoints are covered automatically (extends TC-AUTH-03). **Target:** Sprint 3.

#### NFR-SEC-02 · Role and ownership authorisation

**Statement:** The server shall enforce the role and ownership rules stated in `openapi.yaml`; hiding a menu item in the UI is not considered protection.

**Pass criteria:** For every protected operation, at least one test calls it with a role that is **not** allowed and receives `403 FORBIDDEN`. In particular: `STAFF` cannot access `/reports/*` or `GET /fuel/anomalies` (TC-FUEL-09), cannot verify licences (TC-ELG-05) and cannot read another user's reservation (TC-RES-07). A role change takes effect at the next login.

**Verification:** Role-matrix integration test (operation × role → expected status) kept next to the API tests; the matrix is reviewed against the `openapi.yaml` descriptions by the Lead Architect. **Target:** Sprint 3 for Must endpoints, Final for all.

#### NFR-SEC-03 · Password and credential handling

**Statement:** Passwords shall never be stored or returned in a recoverable form.

**Pass criteria:** Passwords are stored only as Argon2id hashes; passwords shorter than 8 characters are rejected with `400 VALIDATION_ERROR`; no API response contains a password or hash field; unknown email and wrong password both return `401 INVALID_CREDENTIALS` with the same body.

**Verification:** Unit test on the hashing function; integration tests TC-AUTH-01/02 extended to compare the two `401` bodies; database inspection of a seeded user *(new: TC-NFR-SEC-03)*. **Target:** Sprint 3.

#### NFR-SEC-04 · Input validation and safe errors

**Statement:** Invalid input shall be rejected with a controlled error, and errors shall not leak internal details.

**Pass criteria:** Malformed or out-of-range input returns `400 VALIDATION_ERROR` with field-level `errors` (ADR-003); SQL-injection-style strings (for example `' OR 1=1 --`) in text fields and query parameters are stored or rejected as normal data and never change the result set; no error response contains a stack trace, SQL text, file path or library name.

**Verification:** Negative integration tests on login, reservation and fuel receipt endpoints *(new: TC-NFR-SEC-04)*; a check in the shared test helper that fails any test whose error body contains `Traceback` or `sqlalchemy`. **Target:** Sprint 3.

#### NFR-SEC-05 · Personal data, secrets and dependencies

**Statement:** FleetSync shall protect personal data under KVKK and keep secrets and vulnerable dependencies out of the release.

**Pass criteria:**
- Licence numbers and licence details are returned only to the owner and to `FLEET_MANAGER`; other roles receive `403` or a response without those fields.
- Application logs never contain passwords, JWTs or `JWT_SECRET` (shared with NFR-OPS-02).
- Demo and test data use invented people only.
- `pip-audit` and `npm audit` report **no high or critical vulnerabilities** in the release dependencies; SonarQube reports **0 open vulnerabilities** of severity critical or blocker.

**Verification:** Integration test for licence visibility *(new: TC-NFR-SEC-05)*; log inspection during the E2E run; dependency audit output and SonarQube summary attached to the Final report. **Target:** Sprint 3 (licence visibility), Final (audits).

### 4.3 Accessibility and usability

#### NFR-ACC-01 · Accessibility baseline (WCAG 2.1 AA)

**Statement:** The screens used in the jury demo shall meet a WCAG 2.1 level AA baseline.

**Pass criteria:** On the login, trip request and recommendation, ride join, pickup/return checklist, maintenance alerts and reports screens:
- automated accessibility scan reports **0 serious or critical violations**;
- Lighthouse accessibility score **≥ 90**;
- text contrast is at least **4.5:1** (3:1 for large text and UI controls);
- every form field has a visible label, and validation errors are shown as text next to the field.

**Verification:** `axe-core` scan run from the Playwright E2E suite on each demo screen *(new: TC-NFR-ACC-01)*; Lighthouse report; contrast of the Figma colour palette checked before implementation. **Target:** Figma palette check in Sprint 2 review; automated scan in Final.

#### NFR-ACC-02 · Keyboard use and non-colour status

**Statement:** The main demo flow shall be usable without a mouse, and status information shall not rely on colour alone (`ui_ux_flow_and_dashboard.md` §5).

**Pass criteria:** Demo steps 1–6 can be completed using only the keyboard (Tab, Shift+Tab, Enter, Space, Esc) with a visible focus indicator; vehicle, reservation and alert statuses always show the status text (`AVAILABLE`, `IN_MAINTENANCE`, `DUE`, …) next to any colour or icon.

**Verification:** Manual keyboard walkthrough recorded in the test report; review of Figma screens for status text. **Target:** Figma review in Sprint 2; walkthrough in Final.

#### NFR-USE-01 · Fast vehicle request (goal G4)

**Statement:** A staff member shall be able to complete a valid vehicle request quickly without training.

**Pass criteria:** In a usability test with **at least 5 participants** who have not seen the screens before, at least **4 of 5** complete a valid trip request and reservation in **under 2 minutes** (G4 in `system_vision.md`). The screens remain usable at **360 px** and **1280 px** viewport widths.

**Verification:** Timed task with the Figma prototype in Sprint 2/3, repeated with the real application for Final; results (time per participant, problems seen) recorded in the test report. **Target:** Prototype test before Sprint 3 implementation; application test in Final.

### 4.4 Reliability and data consistency

#### NFR-REL-01 · No double booking under concurrency (goal G2)

**Statement:** The system shall never store two overlapping `CONFIRMED`/`ACTIVE` reservations for the same vehicle, or more passengers than free seats, even under concurrent requests (ADR-004).

**Pass criteria:** Two concurrent `POST /reservations` for the same vehicle and period return **exactly one `201` and one `409 RESERVATION_CONFLICT`**; repeated **20 times**, the database contains **0** overlapping reservations. Two concurrent joins for the last free seat return one `201` and one `422 SEAT_CAPACITY_EXCEEDED`. Back-to-back periods are still accepted (TC-RES-03).

**Verification:** Concurrency integration tests against PostgreSQL *(new: TC-RES-11, TC-POOL-07)*; SQL check for overlaps after the run. **Target:** Sprint 3.

#### NFR-REL-02 · Maintenance rules are applied atomically (goals G1, G3)

**Statement:** A return that crosses a service threshold shall always create the alert and change the vehicle status, or change nothing.

**Pass criteria:** In 100% of tests where the return odometer reaches the threshold, the response contains the alert, the alert is `OPEN` and the vehicle is `IN_MAINTENANCE` (TC-MNT-06/07); if alert creation fails (simulated error), the return is rolled back and the reservation stays `ACTIVE`. No reservation can start with a vehicle that is blocked by the 100 km safety buffer (TC-REC-01, TC-RES-04).

**Verification:** Integration tests including one fault-injection test *(new: TC-MNT-11)*. **Target:** Sprint 3.

#### NFR-REL-03 · Consistent, contract-conformant errors

**Statement:** All error responses shall follow ADR-003 so that the frontend and tests can rely on them.

**Pass criteria:** **100%** of error responses observed in the integration test suite have `Content-Type: application/problem+json`, the fields `type`, `title`, `status` and `code`, and a `code` value from the `ErrorCode` enum in `openapi.yaml`. Successful responses validate against their `openapi.yaml` schema.

**Verification:** A shared assertion helper used by every API test, plus schema validation of responses against `openapi.yaml`. **Target:** Sprint 3.

#### NFR-REL-04 · Stable demo run

**Statement:** The jury demo journey shall run reliably from a clean start.

**Pass criteria:** The automated E2E demo test (TC-E2E-01 to TC-E2E-05, US-50) passes in **5 consecutive runs** on a freshly started stack with seed data, with no retries.

**Verification:** CI or local run log of 5 consecutive passes, attached to the Final report. Recovery after restarting services is covered by NFR-OPS-05. **Target:** Final.

### 4.5 Test quality and maintainability

#### NFR-TEST-01 · Unit-test coverage

**Statement:** Backend code shall be covered by automated unit tests.

**Pass criteria:** Backend line coverage measured by `pytest-cov` is **≥ 50%** (course requirement) and CI fails below it (NFR-OPS-06, US-49). Team target for the business-rule modules `maintenance`, `reservation`, `handover` and `fuel`: **≥ 70%**. Frontend coverage from Vitest is published but not used as a gate.

**Verification:** Coverage report published in each PR's CI run; per-module table in the Sprint 3 and Final reports. **Target:** Sprint 3.

#### NFR-TEST-02 · Acceptance-criteria coverage

**Statement:** Every Must user story shall be verified by tests derived from its acceptance criteria.

**Pass criteria:** Sprint 2: every Must story has at least one test case in the test plan (including US-03, US-07, US-08, US-14, US-18). Sprint 3: every Must story in the MVP has at least one automated test. Final: **100%** of Must acceptance criteria have at least one automated test, shown in the traceability matrix (story → endpoint → test → PR).

**Verification:** Traceability section of `test_plans_and_coverage.md` and the SRS traceability matrix. **Target:** Sprint 2 / Sprint 3 / Final as stated.

#### NFR-TEST-03 · Realistic integration and end-to-end testing

**Statement:** Integration tests shall run against the same database engine as production, and the demo journey shall be tested end to end.

**Pass criteria:** Integration tests use PostgreSQL 16 in Docker (Testcontainers), not SQLite (required by ADR-004); they run in CI on every PR to `develop` (US-51); the Playwright E2E test of the demo journey runs in CI before each submission (US-50).

**Verification:** CI workflow files and run logs. **Target:** Sprint 3 (integration), Final (E2E).

#### NFR-TEST-04 · Static analysis and open defects

**Statement:** The release shall have no known critical quality problems.

**Pass criteria:** SonarQube quality gate **passed**, with **0 blocker and 0 critical issues** and duplicated lines **< 5%** on new code; **0 open critical or blocker defects** (GitHub issues labelled `bug`) at the Final demo.

**Verification:** SonarQube summary and a filtered issue list attached to the Final report. **Target:** Final.

### 4.6 QA traceability

| NFR | Main evidence | Backlog / ADR link | Review |
|---|---|---|---|
| PERF-01 | Locust report | US-46, US-47 | QA + Backend + Architect |
| PERF-02 | Pagination integration tests | `openapi.yaml` | QA + Backend |
| PERF-03 | Lighthouse report | US-38 – US-43 | QA + Frontend |
| SEC-01 | Parametrised auth test | US-01, ADR-005 | QA + Architect |
| SEC-02 | Role-matrix test | US-01, US-04, US-21, US-31, US-34 – US-36 | QA + PO |
| SEC-03 | Hashing unit test, auth tests | US-01, US-02, ADR-005 | QA + PO |
| SEC-04 | Negative input tests | ADR-003 | QA + Backend |
| SEC-05 | Licence visibility test, audits, SonarQube | US-03, US-04, §10 KVKK | QA + DevOps |
| ACC-01, ACC-02 | axe / Lighthouse report, keyboard walkthrough | US-38 – US-43 | QA + Frontend |
| USE-01 | Usability test results | G4, US-40 | QA + Frontend + PO |
| REL-01 | Concurrency tests | US-20, US-24, ADR-004 | QA + Backend |
| REL-02 | Return / maintenance tests | US-12, US-13, G1, G3 | QA + Architect |
| REL-03 | Problem-details assertion, schema validation | ADR-003 | QA + Backend |
| REL-04 | 5 consecutive E2E passes | US-50 | QA + DevOps |
| TEST-01 | Coverage report | US-49 | QA + DevOps |
| TEST-02 | Traceability matrix | All Must stories | QA + PO |
| TEST-03 | CI workflows | US-50, US-51, ADR-004 | QA + DevOps |
| TEST-04 | SonarQube summary, issue list | Final readiness | QA + DevOps |

## 5. Sprint 2 review and open decisions

| Item | Requested owner | Status |
|---|---|---|
| Review operational acceptance targets for feasibility | Ali Eren Kurt | Done — feasible for Sprint 3 / Final as targeted. OPS-05 readiness check is `GET /api/v1/health` (200 when the database answers, 503 otherwise), already in the backend skeleton (#249). |
| Approve localhost HTTP vs public HTTPS rule (DD-2) | Ali Eren Kurt + Deniz Alp Oniki | Approved by the Architect — HTTP on localhost for the demo, HTTPS for any public environment (NFR-OPS-08) |
| Confirm API/JWT environment-variable names (DD-3) | Ali Eren Kurt + Deniz Alp Oniki | Confirmed by the Architect — names in NFR-OPS-02; `.env.example` updated with DD-1 |
| Review backup/restore method (DD-4) | Deniz Alp Oniki + Abdullah Tecimen | Open |
| Add measurable QA metrics (section 4) | Abdullah Tecimen | Drafted — in review |
| Approve QA numeric targets (PERF-01 load profile, 70% module coverage, WCAG 2.1 AA) | Ali Eren Kurt + Ahmet Can Vurmaz | Approved by the Architect — 20 virtual users fit assumption A6; 70% for the business-rule modules is a team target reported per module, the CI gate stays at 50%; WCAG 2.1 AA for the demo screens. PO approval pending. |
| Confirm performance targets are realistic for the reservation and recommendation queries | Ahmet Tarık Orhan | Open |
| Decide pagination for fuel receipts, anomalies and expenses (PERF-02) | Ali Eren Kurt | Decided — no pagination in release 1; the server bounds them to a default of 92 days and a maximum of 366 days (NFR-PERF-02, `openapi.yaml`) |
| Check Figma palette contrast and status text (ACC-01, ACC-02) | Mustafa Düşünceli + Abdullah Tecimen | Open |
| Add the *(new)* test case IDs from section 4 to the test plan | Abdullah Tecimen | Open |
| Reconcile with SRS and traceability | Ahmet Can Vurmaz | Open |

**Sprint 2 exit condition:** Requirement IDs, measurable acceptance criteria and verification methods are documented and reviewed. Do not mark future operational implementation as complete until its tests have actually run.
