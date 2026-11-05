# FleetSync · Sprint 1 Report · Project Foundation

> SENG 321 · Weeks 1–2 · Tag: `sprint-1` · Weight: 15%
> Owner: Mehmet Umut Oğuzcan (Scrum Master). Related: [`../raci_matrix.md`](../raci_matrix.md) · [`../git_flow.md`](../git_flow.md) · [`impediment_log.md`](impediment_log.md)

## 1. Sprint goal

Agree on the first version of FleetSync: problem, vision and system boundary, OpenAPI contract, initial backlog, team roles, and a working GitHub process (protected branches, templates, review rules).

## 2. Team

| # | Role | Member | GitHub |
|---|---|---|---|
| 1 | Product Owner & Requirements Engineer | Ahmet Can Vurmaz | `@Chadde7` |
| 2 | Scrum Master & Agile Process Coach | Mehmet Umut Oğuzcan | `@umt06-1` |
| 3 | Lead Software Architect & Technical Lead | Ali Eren Kurt | `@AliErenJ` |
| 4 | Quality Assurance & Test Automation Engineer | Abdullah Tecimen | `@TheTeci` |
| 5 | DevOps & CI/CD Infrastructure Engineer | Deniz Alp Oniki | `@denizalponiki` |
| 6 | Implementation & Integration Engineer (Backend) | Ahmet Tarık Orhan | `@ahmettarikorhan` |
| 7 | Implementation & Integration Engineer (Frontend) | Mustafa Düşünceli | `@mustafadusunceli` |

## 3. Meeting calendar

| Meeting | When | Length | Where | Output |
|---|---|---|---|---|
| Sprint planning | First day of each sprint, 11:00 | 30 min | micup | This file, §4 |
| Stand-up | Twice a week: Saturday 11:00 and Sunday 12:00 | 2 hours | micup | §5 |
| Sprint review | Last day of the sprint, 10:00 | 30 min | micup | §6 |
| Retrospective | Right after the review | 30 min | same | §7 |

Stand-up questions: What did I finish since the last stand-up? What will I do next? What blocks me? Blockers go to [`impediment_log.md`](impediment_log.md).

## 4. Sprint planning · Sprint backlog

| Deliverable | A / R | Issue | PR | Status |
|---|---|---|---|---|
| Project proposal and problem definition (`problem_definition.md`) | Ahmet Can Vurmaz | | #14, #16 | Done |
| System vision and boundary (`system_vision.md`) | Ahmet Can Vurmaz / Ali Eren Kurt | | #10, #12, #24 | Done |
| OpenAPI contract (`openapi.yaml`, `api_usage.md`) | Ali Eren Kurt + module owners | | #14, #22, #119 | Done |
| Initial backlog (`product_backlog.md`) | Ahmet Can Vurmaz | | #17 | Done |
| Test plan and QA templates | Abdullah Tecimen | | #9 | Done |
| Roles and RACI matrix (`raci_matrix.md`) | Mehmet Umut Oğuzcan | | #26, #44 | Done |
| Git-Flow rules (`git_flow.md`) | Mehmet Umut Oğuzcan | | #26 | Done |
| `CODEOWNERS` and user story template | Mehmet Umut Oğuzcan | | #28, #29, #45, #48 | Done |
| Sprint report and impediment log (`sprint-reports/`) | Mehmet Umut Oğuzcan | #131 | #26, #30–#35, #132 | Done |
| GitHub Projects board (Backlog, Ready, In Progress, Review, Done) | Mehmet Umut Oğuzcan | | – | Done |
| Branch protection on `main` and `develop` | Mehmet Umut Oğuzcan / Deniz Alp Oniki | | – | In Progress |
| CI: OpenAPI lint (`.github/workflows/openapi-lint.yml`) | Deniz Alp Oniki | #36 | #37 | Done |
| C4 level 1 diagram (`system_vision.md` §6) | Ali Eren Kurt | | #120 | Done |
| Reservation and carpool API notes, Prism mock (`carpool_reservation_api.md`) | Ahmet Tarık Orhan | #53 | #54 | Done |
| Screen list, UI/UX flow (`ui_ux_flow_and_dashboard.md`) | Mustafa Düşünceli | #39 | #109 | Done |
| CI/CD and reporting documentation (`ci_cd_and_cost_reporting_api.md`) | Deniz Alp Oniki | #67 | #68 | Done |
| Handover user stories as GitHub issues (US-26, US-27, US-28) | Mehmet Umut Oğuzcan | #128, #129, #130 | – | Done |
| `docker-compose.yml` skeleton | Deniz Alp Oniki | #133 | #134 | Done |
| First ADR (`docs/adr/ADR-001-python-fastapi.md`) | Ali Eren Kurt | #135 | #136 | Done |
| `develop` → `main` merge and `sprint-1` tag | Deniz Alp Oniki | | | In progress |

## 5. Stand-up records

### Stand-up · 2026-10-31 (Saturday, Micup)
Present: all seven members · Absent: none
Format: each member presented the Sprint 1 task they own.

| Member | Sprint 1 task presented | Blocker |
|---|---|---|
| Ahmet Can Vurmaz | Project proposal, problem definition and initial product backlog | – |
| Mehmet Umut Oğuzcan | RACI matrix, Git-Flow rules, repository templates and sprint records | – |
| Ali Eren Kurt | System vision, C4 level 1 and the OpenAPI contract | – |
| Abdullah Tecimen | Test strategy, test plan and QA issue templates | – |
| Deniz Alp Oniki | Repository setup, CI (OpenAPI lint) and Docker Compose skeleton | – |
| Ahmet Tarık Orhan | Reservation and carpool API paths, Prism mock | – |
| Mustafa Düşünceli | Screen list, UI/UX flow and consumer review of the OpenAPI contract | – |

<!-- Copy this block for every stand-up. Write only what was actually said. -->

### Stand-up · YYYY-MM-DD
Present: …  · Absent: …

| Member | Done since last stand-up | Next | Blocker |
|---|---|---|---|
| Ahmet Can Vurmaz | | | |
| Mehmet Umut Oğuzcan | | | |
| Ali Eren Kurt | | | |
| Abdullah Tecimen | | | |
| Deniz Alp Oniki | | | |
| Ahmet Tarık Orhan | | | |
| Mustafa Düşünceli | | | |

## 6. Sprint review

<!-- Fill in at the end of the sprint. -->
- Delivered: …
- Not delivered (moved to Sprint 2): …
- Feedback: …

## 7. Retrospective

<!-- Fill in at the end of the sprint; the Sprint 2 report starts by checking these actions. -->

| Went well | To improve | Action (owner) |
|---|---|---|
| | | |

## 8. Weekly contribution check

Commits: non-merge commits on `develop`. PRs opened, reviews (on other members' PRs) and issues opened: GitHub search counts.

| Member | Commits | PRs opened | Reviews | Issues | Checked on |
|---|---|---|---|---|---|
| Ahmet Can Vurmaz | 3 | 3 | 16 | 17 | 2026-11-05 |
| Mehmet Umut Oğuzcan | 17 | 16 | 4 | 7 | 2026-11-05 |
| Ali Eren Kurt | 11 | 12 | 24 | 13 | 2026-11-05 |
| Abdullah Tecimen | 10 | 7 | 11 | 15 | 2026-11-05 |
| Deniz Alp Oniki | 20 | 15 | 7 | 11 | 2026-11-05 |
| Ahmet Tarık Orhan | 2 | 2 | 3 | 11 | 2026-11-05 |
| Mustafa Düşünceli | 1 | 1 | 2 | 9 | 2026-11-05 |

Every member has at least one commit, PR, review and issue (IMP-03 closed).

## 9. Submission evidence list

| Item | Link |
|---|---|
| Repository | https://github.com/denizalponiki/Fleet-Tracking-System |
| Projects board | https://github.com/users/umt06-1/projects/2 |
| Tag | https://github.com/denizalponiki/Fleet-Tracking-System/releases/tag/sprint-1 |
| Problem definition | [`docs/problem_definition.md`](../problem_definition.md) |
| System vision | [`docs/system_vision.md`](../system_vision.md) |
| OpenAPI contract | [`docs/openapi.yaml`](../openapi.yaml) |
| Product backlog | [`docs/product_backlog.md`](../product_backlog.md) |
| Test plan | [`docs/test_plans_and_coverage.md`](../test_plans_and_coverage.md) |
| RACI | [`docs/raci_matrix.md`](../raci_matrix.md) |
| Git-Flow rules | [`docs/git_flow.md`](../git_flow.md) |
| Templates | [`.github/`](../../.github) |
| ADR-001 | [`docs/adr/ADR-001-python-fastapi.md`](../adr/ADR-001-python-fastapi.md) |
| Docker Compose skeleton | [`docker-compose.yml`](../../docker-compose.yml) |
| CI/CD documentation | [`docs/ci_cd_and_cost_reporting_api.md`](../ci_cd_and_cost_reporting_api.md) |
| Reservation and carpool API notes | [`docs/carpool_reservation_api.md`](../carpool_reservation_api.md) |
| UI/UX flow | [`docs/ui_ux_flow_and_dashboard.md`](../ui_ux_flow_and_dashboard.md) |
| Handover epic and user stories | [#74](https://github.com/denizalponiki/Fleet-Tracking-System/issues/74) · [#128](https://github.com/denizalponiki/Fleet-Tracking-System/issues/128) · [#129](https://github.com/denizalponiki/Fleet-Tracking-System/issues/129) · [#130](https://github.com/denizalponiki/Fleet-Tracking-System/issues/130) |
