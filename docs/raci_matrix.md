# FleetSync · Team Roles and RACI Matrix

> SENG 321 · Sprint 1 deliverable 4. Owner: Mehmet Umut Oğuzcan (Scrum Master). Drafted by: Ali Eren Kurt. Last updated: 2026-10-25.
> Repository: https://github.com/denizalponiki/Fleet-Tracking-System · License: MIT
> Fill in the GitHub usernames marked `@?`; they must match the ones in `CODEOWNERS`.

## 1. Team and roles

| # | Role | Member | GitHub | Code module | Rubric area owned |
|---|------|--------|--------|-------------|-------------------|
| 1 | Product Owner & Requirements Engineer | Ahmet Can Vurmaz | `@?` | `identity` (driver profile, licence / eligibility checks, login) | Requirements & backlog (20) |
| 2 | Scrum Master & Agile Process Coach | Mehmet Umut Oğuzcan | `@?` | `handover` (pickup / return checklist, damage reports) | Process evidence, individual contribution tracking |
| 3 | Lead Software Architect & Technical Lead | Ali Eren Kurt | `@?` | `maintenance` (predictive maintenance rule engine), `vehicle` | Architecture C4 + UML (25), defence (20) |
| 4 | Quality Assurance & Test Automation Engineer | Abdullah Tecimen | `@?` | `fuel` (fuel receipts, expenses, anomalies) | Testing, coverage ≥ 50% |
| 5 | DevOps & CI/CD Infrastructure Engineer | Deniz Alp Oniki | `@denizalponiki` | `reporting` (cost, carbon, utilisation) | Live demo with Docker (20) |
| 6 | Implementation & Integration Engineer (Backend & API) | Ahmet Tarık Orhan | `@?` | `reservation`, `carpool`, `locations` | Primary user journey |
| 7 | Implementation & Integration Engineer (Frontend & UI) | Mustafa Düşünceli | `@?` | `frontend` (all screens) | Demo UI, Figma |

Every member writes the unit tests for their own module. QA owns the test strategy and the integration and E2E tests. Tests in QA's own module (`fuel`) are reviewed by another member.

## 2. Role responsibilities

### #1 Product Owner & Requirements Engineer · Ahmet Can Vurmaz
- Project proposal, system vision, scope (in / out).
- Personas and user stories for the fleet manager, staff member and maintenance officer; every story has Given/When/Then acceptance criteria and story points.
- Backlog prioritisation (MoSCoW), sprint goals, stakeholder validation.
- SRS and traceability matrix (story → endpoint → test → PR).
- Presents the scenario during the jury demo.
- **Code:** `identity`: JWT login, role-based authorisation, licence class and validity checks (`/auth/*`, `/users`, `/drivers/*`).

### #2 Scrum Master & Agile Process Coach · Mehmet Umut Oğuzcan
- GitHub organisation, GitHub Projects board, issue / PR templates.
- This RACI document and the Git-Flow rules document.
- Sprint planning, stand-up, review and retrospective records (`docs/sprint-reports/`), impediment log, burndown.
- Evidence list for every submission: tag, issue, PR and diagram links.
- Weekly contribution check: no member should have an empty commit / PR / review history.
- **Code:** `handover`: checklist, mileage entry, damage reports, publishing `TripCompletedEvent` (`/reservations/{id}/pickup`, `/reservations/{id}/return`, `/damage-reports`, `/checklist-templates`).

### #3 Lead Software Architect & Technical Lead · Ali Eren Kurt
- Architecture decisions and ADRs (`docs/adr/`).
- C4 (levels 1, 2, 3), UML (class, sequence, state, deployment), ER diagram and database schema.
- Consistency of `docs/openapi.yaml`: naming, shared schemas, error format, versioning. Approves every PR that touches it.
- Repository skeleton, module boundaries, ArchUnit rules, coding standard, code review leadership.
- Leads the architectural defence in front of the jury.
- **Code:** `maintenance` + `vehicle`: rule engine, alerts, maintenance records, vehicle state machine (`/vehicles*`, `/maintenance/*`).

### #4 Quality Assurance & Test Automation Engineer · Abdullah Tecimen
- Test strategy, test plan, test case catalogue derived from acceptance criteria.
- Thorough unit and E2E tests for fuel consumption anomalies, mileage limit violations and reservation conflicts.
- Integration tests (Testcontainers), contract tests, Playwright E2E.
- Coverage tracking (≥ 50%), defect tracking, final test report.
- **Code:** `fuel`: fuel receipts, expenses, consumption and anomalies (`/fuel-receipts`, `/fuel/anomalies`, `/expenses`, `/vehicles/{id}/consumption`).

### #5 DevOps & CI/CD Infrastructure Engineer · Deniz Alp Oniki
- `docker-compose.yml`, Dockerfiles, seed data, `demo-reset`.
- GitHub Actions: OpenAPI lint, build, tests, coverage gate.
- Branch protection, release tags, SonarQube setup and report.
- **Code:** `reporting`: cost, carbon, utilisation, summary (`/reports/*`).

### #6 Implementation & Integration Engineer (Backend & API) · Ahmet Tarık Orhan
- Reservation and carpool sections of the OpenAPI contract; exposes the Prism mock to the frontend.
- Cross-module integration and integration defect fixes; backend technical documentation.
- Second reviewer on other backend PRs.
- **Code:** `reservation` + `carpool`: vehicle recommendation, reservations, conflict prevention, ride-sharing matching (`/vehicles/recommendations`, `/reservations*`, `/rides/matches`, `/locations`).

### #7 Implementation & Integration Engineer (Frontend & UI) · Mustafa Düşünceli
- Figma prototypes, user-flow diagrams, design system.
- Reviews the OpenAPI contract from the consumer's side.
- Moves the UI from the mock to the real API; end-to-end integration.
- **Code:** vehicle status cards, request and recommendation screen, carpool, checklist, maintenance calendar, fuel form, reports.

## 3. RACI matrix

**R** does the work · **A** owns the outcome and approves it (one A per row) · **C** consulted before the decision · **I** informed of the outcome

### 3.1 Sprint 1 deliverables

| Deliverable | #1 PO<br>Ahmet Can | #2 SM<br>M. Umut | #3 Arch<br>Ali Eren | #4 QA<br>Abdullah | #5 DevOps<br>Deniz Alp | #6 BE<br>A. Tarık | #7 FE<br>Mustafa |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Project proposal and problem definition | **A/R** | C | C | I | I | C | C |
| Open-source license selection (MIT) | **A** | I | R | I | C | I | I |
| System vision and system boundary | **A** | I | R | C | I | C | C |
| OpenAPI contract (integrity, shared schemas) | C | C | **A/R** | C | C | R | C |
| OpenAPI · identity paths | R | I | A | C | I | C | C |
| OpenAPI · handover paths | C | R | A | C | I | C | C |
| OpenAPI · vehicle + maintenance paths | C | I | **A/R** | C | I | C | C |
| OpenAPI · fuel paths | C | I | A | R | I | C | C |
| OpenAPI · reports paths | C | I | A | C | R | C | C |
| OpenAPI · reservation + carpool paths | C | I | A | C | I | R | C |
| Role assignments and RACI matrix | C | **A/R** | C | I | I | I | I |
| GitHub organisation, Projects board, templates | I | **A/R** | C | I | R | I | I |
| Git-Flow rules and branch protection | I | **A** | C | C | R | I | I |
| Initial backlog (epics, stories, acceptance criteria, estimates) | **A/R** | C | C | C | I | C | C |
| CI: OpenAPI lint | I | I | C | C | **A/R** | I | I |
| Sprint 1 submission evidence list | C | **A/R** | C | I | C | I | I |

### 3.2 Whole project (Sprint 2 – Final)

| Deliverable | #1 PO<br>Ahmet Can | #2 SM<br>M. Umut | #3 Arch<br>Ali Eren | #4 QA<br>Abdullah | #5 DevOps<br>Deniz Alp | #6 BE<br>A. Tarık | #7 FE<br>Mustafa |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| SRS and refined backlog | **A/R** | C | C | C | I | C | C |
| Non-functional requirements and quality measures | C | I | **A** | R | R | C | C |
| Figma prototypes and user flows | C | I | C | I | I | C | **A/R** |
| C4, UML, ER, ADRs | I | I | **A/R** | C | C | C | C |
| Database schema and migrations | I | I | **A/R** | I | C | C | I |
| MVP (working product) | R | R | **A/R** | R | R | R | R |
| identity module | **A/R** | I | C | C | I | C | I |
| handover module | I | **A/R** | C | C | I | C | C |
| maintenance + vehicle module | I | I | **A/R** | C | I | C | C |
| fuel module | I | I | C | **A/R** | I | C | C |
| reporting module | C | I | C | C | **A/R** | C | C |
| reservation + carpool module | C | I | C | C | I | **A/R** | C |
| Frontend screens | C | I | C | C | I | C | **A/R** |
| CI/CD, Docker, seed data | I | I | C | C | **A/R** | C | C |
| Unit test coverage ≥ 50% | R | R | R | **A/R** | R | R | R |
| Integration + E2E test report | I | I | C | **A/R** | C | R | R |
| SonarQube and technical debt report | I | I | R | C | **A/R** | C | C |
| Sprint records, impediment log, burndown | C | **A/R** | C | C | C | C | C |
| Live demo scenario | **A/R** | C | C | C | R | R | R |
| Architectural defence | C | C | **A/R** | C | C | C | C |
| Peer assessment organisation | I | **A/R** | I | I | I | I | I |

## 4. Decision and approval rules

- **Scope and priority:** the PO decides and consults the Architect when there is technical impact.
- **Technical and architectural decisions:** the Architect decides and records an ADR. If a decision affects a module, its owner is consulted first.
- **API contract changes:** open a PR; the affected module owners and the Architect approve it. After the contract is tagged v1.0 in Sprint 2, breaking changes require a new version.
- **Code review:** every PR needs at least one approval, and nobody approves their own PR. Changes to `docs/openapi.yaml`, `docs/adr/` and cross-module interfaces require the Architect's approval.
- **Unresolved disagreements:** first discuss with the row's A. If that does not resolve it, the Scrum Master brings it to the weekly meeting and the team decides.

## 5. Draft CODEOWNERS

For `.github/CODEOWNERS`, with real GitHub usernames:

```text
# Default: the Lead Architect reviews every PR
*                                         @arch-github
/docs/openapi.yaml                        @arch-github @backend-github
/docs/adr/                                @arch-github
/src/backend/**/identity/                 @po-github
/src/backend/**/handover/                 @sm-github
/src/backend/**/vehicle/                  @arch-github
/src/backend/**/maintenance/              @arch-github
/src/backend/**/fuel/                     @qa-github
/src/backend/**/reporting/                @denizalponiki
/src/backend/**/reservation/              @backend-github
/src/backend/**/carpool/                  @backend-github
/src/frontend/                            @frontend-github
/src/e2e/                                 @qa-github
/infra/                                   @denizalponiki
/.github/workflows/                       @denizalponiki
/docker-compose.yml                       @denizalponiki
/docs/sprint-reports/                     @sm-github
```
