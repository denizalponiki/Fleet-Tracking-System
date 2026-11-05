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
| OpenAPI contract (`openapi.yaml`, `api_usage.md`) | Ali Eren Kurt + module owners | | #14, #22 | Done |
| Initial backlog (`product_backlog.md`) | Ahmet Can Vurmaz | | #17 | Done |
| Test plan and QA templates | Abdullah Tecimen | | #9 | Done |
| Roles and RACI matrix (`raci_matrix.md`) | Mehmet Umut Oğuzcan | | #26 | Done |
| Git-Flow rules (`git_flow.md`) | Mehmet Umut Oğuzcan | | #26 | Done |
| `CODEOWNERS` and user story template | Mehmet Umut Oğuzcan | | #28, #29 | Done |
| GitHub Projects board (Backlog, Ready, In Progress, Review, Done) | Mehmet Umut Oğuzcan | | – | Not started |
| Branch protection on `main` and `develop` | Mehmet Umut Oğuzcan / Deniz Alp Oniki | | – | In Progress |
| CI: OpenAPI lint (`.github/workflows/openapi-lint.yml`) | Deniz Alp Oniki | #36 | #37 | Done |
| C4 level 1 diagram (`system_vision.md` §6) | Ali Eren Kurt | | | Done |
| Reservation and carpool API notes, Prism mock (`carpool_reservation_api.md`) | Ahmet Tarık Orhan | #53 | #54 | Done |
| Screen list, UI/UX flow (`ui_ux_flow_and_dashboard.md`) | Mustafa Düşünceli | #39 | #109 | Done |
| CI/CD and reporting documentation (`ci_cd_and_cost_reporting_api.md`) | Deniz Alp Oniki | #67 | #68 | Done |
| Handover user stories as GitHub issues (US-26, US-27, US-28) | Mehmet Umut Oğuzcan | #128, #129, #130 | – | Done |
| `docker-compose.yml` skeleton | Deniz Alp Oniki | | | Not started |
| First ADRs (`docs/adr/`) | Ali Eren Kurt | | | Not started |
| `develop` → `main` merge and `sprint-1` tag | Deniz Alp Oniki | | | Not started |

## 5. Stand-up records

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

| Member | Commits | PRs opened | Reviews | Issues | Checked on |
|---|---|---|---|---|---|
| Ahmet Can Vurmaz | | | | | |
| Mehmet Umut Oğuzcan | | | | | |
| Ali Eren Kurt | | | | | |
| Abdullah Tecimen | | | | | |
| Deniz Alp Oniki | | | | | |
| Ahmet Tarık Orhan | | | | | |
| Mustafa Düşünceli | | | | | |

## 9. Submission evidence list

| Item | Link |
|---|---|
| Repository | https://github.com/denizalponiki/Fleet-Tracking-System |
| Tag | https://github.com/denizalponiki/Fleet-Tracking-System/releases/tag/sprint-1 |
| Problem definition | [`docs/problem_definition.md`](../problem_definition.md) |
| System vision | [`docs/system_vision.md`](../system_vision.md) |
| OpenAPI contract | [`docs/openapi.yaml`](../openapi.yaml) |
| Product backlog | [`docs/product_backlog.md`](../product_backlog.md) |
| Test plan | [`docs/test_plans_and_coverage.md`](../test_plans_and_coverage.md) |
| RACI | [`docs/raci_matrix.md`](../raci_matrix.md) |
| Git-Flow rules | [`docs/git_flow.md`](../git_flow.md) |
| Templates | [`.github/`](../../.github) |
| CI/CD documentation | [`docs/ci_cd_and_cost_reporting_api.md`](../ci_cd_and_cost_reporting_api.md) |
| Reservation and carpool API notes | [`docs/carpool_reservation_api.md`](../carpool_reservation_api.md) |
| UI/UX flow | [`docs/ui_ux_flow_and_dashboard.md`](../ui_ux_flow_and_dashboard.md) |
| Handover epic and user stories | [#74](https://github.com/denizalponiki/Fleet-Tracking-System/issues/74) · [#128](https://github.com/denizalponiki/Fleet-Tracking-System/issues/128) · [#129](https://github.com/denizalponiki/Fleet-Tracking-System/issues/129) · [#130](https://github.com/denizalponiki/Fleet-Tracking-System/issues/130) |
