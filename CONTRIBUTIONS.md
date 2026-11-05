# FleetSync · Individual Contributions

> SENG 321 · Team 3 · Sprint 1 (tag [`sprint-1`](https://github.com/denizalponiki/Fleet-Tracking-System/releases/tag/sprint-1))
> Maintained by the Scrum Master. Last updated: 2026-11-05.
> Numbers in the form `#N` link to the issue or pull request with that number in this repository.

| # | Member | Student no. | GitHub | Role |
|---|---|---|---|---|
| 1 | Ahmet Can Vurmaz | 260204318 | [@Chadde7](https://github.com/Chadde7) | Product Owner & Requirements Engineer |
| 2 | Mehmet Umut Oğuzcan | 240201012 | [@umt06-1](https://github.com/umt06-1) | Scrum Master & Agile Process Coach |
| 3 | Ali Eren Kurt | 260201308 | [@AliErenJ](https://github.com/AliErenJ) | Lead Software Architect & Technical Lead |
| 4 | Abdullah Tecimen | 230201073 | [@TheTeci](https://github.com/TheTeci) | Quality Assurance & Test Automation Engineer |
| 5 | Deniz Alp Oniki | 230205048 | [@denizalponiki](https://github.com/denizalponiki) | DevOps & CI/CD Infrastructure Engineer |
| 6 | Ahmet Tarık Orhan | 260201305 | [@ahmettarikorhan](https://github.com/ahmettarikorhan) | Implementation & Integration Engineer (Backend & API) |
| 7 | Mustafa Düşünceli | 260204319 | [@mustafadusunceli](https://github.com/mustafadusunceli) | Implementation & Integration Engineer (Frontend & UI) |

Full responsibilities per role: [`docs/raci_matrix.md`](docs/raci_matrix.md).

## Summary (as of 2026-11-05)

| Member | Commits | PRs opened | Reviews | Issues opened |
|---|---|---|---|---|
| Ahmet Can Vurmaz | 3 | 3 | 18 | 17 |
| Mehmet Umut Oğuzcan | 23 | 21 | 4 | 11 |
| Ali Eren Kurt | 11 | 12 | 28 | 13 |
| Abdullah Tecimen | 10 | 7 | 11 | 15 |
| Deniz Alp Oniki | 20 | 16 | 7 | 11 |
| Ahmet Tarık Orhan | 2 | 2 | 3 | 11 |
| Mustafa Düşünceli | 1 | 1 | 2 | 9 |

Commits = non-merge commits on `develop`. Reviews = reviews on other members' pull requests. Live view: [contributors graph](https://github.com/denizalponiki/Fleet-Tracking-System/graphs/contributors).

---

## 1. Ahmet Can Vurmaz · Product Owner & Requirements Engineer

- **Student no.:** 260204318 · **GitHub:** [@Chadde7](https://github.com/Chadde7)
- **Responsibilities:** project proposal, problem definition and scope; product backlog with epics, user stories and acceptance criteria; backlog prioritisation; code module `identity`.
- **Sprint 1 work:**
  - Project proposal and problem definition: [`docs/problem_definition.md`](docs/problem_definition.md)
  - Initial product backlog (10 epics, user stories with Given/When/Then criteria): [`docs/product_backlog.md`](docs/product_backlog.md)
  - Opened the 10 epic issues (#69–#78) and the identity stories US-01–US-06 (#86–#91)
  - Aligned US-20 with the API contract (409 for the maintenance block): #65 → #66
  - Reviewed and merged teammates' PRs, e.g. #54, #119, #120, #132, #141, #146
- **Pull requests opened:** #16, #17, #66
- **Commits:** [list](https://github.com/denizalponiki/Fleet-Tracking-System/commits/develop?author=Chadde7)
- **Issues:** [opened](https://github.com/denizalponiki/Fleet-Tracking-System/issues?q=is%3Aissue+author%3AChadde7) · [assigned](https://github.com/denizalponiki/Fleet-Tracking-System/issues?q=is%3Aissue+assignee%3AChadde7)

## 2. Mehmet Umut Oğuzcan · Scrum Master & Agile Process Coach

- **Student no.:** 240201012 · **GitHub:** [@umt06-1](https://github.com/umt06-1)
- **Responsibilities:** RACI matrix, Git-Flow rules, repository templates, GitHub Projects board, sprint records and impediment log, submission evidence; code module `handover`.
- **Sprint 1 work:**
  - Roles and RACI matrix: [`docs/raci_matrix.md`](docs/raci_matrix.md) (#26, #44)
  - Git-Flow and contribution rules: [`docs/git_flow.md`](docs/git_flow.md) (#26)
  - `CODEOWNERS` and the user story issue form: [`.github/`](.github) (#28, #29, #45, #47, #48; issue #46)
  - Sprint 1 report, meeting calendar, stand-up record and evidence list: [`docs/sprint-reports/sprint-1.md`](docs/sprint-reports/sprint-1.md) (#30–#35, #132, #139, #141, #143, #146, #149)
  - Impediment log IMP-01 to IMP-05: [`docs/sprint-reports/impediment_log.md`](docs/sprint-reports/impediment_log.md)
  - GitHub Projects board: [FleetSync board](https://github.com/users/umt06-1/projects/2)
  - Handover user stories US-26–US-28 under epic #74: #128, #129, #130
  - Reviewed and merged #40 and #127; prepared this contributions file
- **Pull requests opened:** #26–#35, #44, #45, #47, #48, #132, #139, #141, #143, #146, #147, #149
- **Commits:** [list](https://github.com/denizalponiki/Fleet-Tracking-System/commits/develop?author=umt06-1)
- **Issues:** [opened](https://github.com/denizalponiki/Fleet-Tracking-System/issues?q=is%3Aissue+author%3Aumt06-1) · [assigned](https://github.com/denizalponiki/Fleet-Tracking-System/issues?q=is%3Aissue+assignee%3Aumt06-1)

## 3. Ali Eren Kurt · Lead Software Architect & Technical Lead

- **Student no.:** 260201308 · **GitHub:** [@AliErenJ](https://github.com/AliErenJ)
- **Responsibilities:** system vision and boundary, OpenAPI contract consistency, C4 and UML, architecture decisions, code review leadership; code modules `maintenance` and `vehicle`.
- **Sprint 1 work:**
  - System vision, system boundary and C4 level 1 context diagram: [`docs/system_vision.md`](docs/system_vision.md) (#24, #42, #120)
  - OpenAPI contract and usage guide: [`docs/openapi.yaml`](docs/openapi.yaml), [`docs/api_usage.md`](docs/api_usage.md) (#22, #119, #137)
  - ADR-001, Python / FastAPI backend: [`docs/adr/ADR-001-python-fastapi.md`](docs/adr/ADR-001-python-fastapi.md) (issue #135, PR #136)
  - Maintenance and vehicle stories US-07–US-17: #92–#102
  - Most reviews in the team (28); merged the largest number of Sprint 1 PRs, including the `develop` → `main` release merge #144
- **Pull requests opened:** #18–#22, #24, #42, #119, #120, #136, #137
- **Commits:** [list](https://github.com/denizalponiki/Fleet-Tracking-System/commits/develop?author=AliErenJ)
- **Issues:** [opened](https://github.com/denizalponiki/Fleet-Tracking-System/issues?q=is%3Aissue+author%3AAliErenJ) · [assigned](https://github.com/denizalponiki/Fleet-Tracking-System/issues?q=is%3Aissue+assignee%3AAliErenJ)

## 4. Abdullah Tecimen · Quality Assurance & Test Automation Engineer

- **Student no.:** 230201073 · **GitHub:** [@TheTeci](https://github.com/TheTeci)
- **Responsibilities:** test strategy and plan, test cases from acceptance criteria, coverage tracking, QA reviews; code module `fuel`.
- **Sprint 1 work:**
  - Test plan and coverage strategy: [`docs/test_plans_and_coverage.md`](docs/test_plans_and_coverage.md) (#9, #40, #64, #127)
  - Bug report and test task issue forms (issue #49, PR #51)
  - QA findings raised as issues and tracked to closure: #41, #43, #63, #67, #126
  - Fuel and quality stories US-29–US-32, US-49–US-51: #79–#85
  - Reviewed and merged teammates' PRs, e.g. #10, #14, #16, #17, #45, #48, #108
- **Pull requests opened:** #9, #40, #51, #64, #127
- **Commits:** [list](https://github.com/denizalponiki/Fleet-Tracking-System/commits/develop?author=TheTeci)
- **Issues:** [opened](https://github.com/denizalponiki/Fleet-Tracking-System/issues?q=is%3Aissue+author%3ATheTeci) · [assigned](https://github.com/denizalponiki/Fleet-Tracking-System/issues?q=is%3Aissue+assignee%3ATheTeci)

## 5. Deniz Alp Oniki · DevOps & CI/CD Infrastructure Engineer

- **Student no.:** 230205048 · **GitHub:** [@denizalponiki](https://github.com/denizalponiki)
- **Responsibilities:** repository setup, branch protection, CI/CD pipeline, Docker Compose, release tags; code module `reporting`.
- **Sprint 1 work:**
  - Repository, README and documentation index (#1–#7, #110)
  - Branch protection on `main` and `develop` (repository ruleset "Branch Protection")
  - OpenAPI lint CI workflow: [`.github/workflows/openapi-lint.yml`](.github/workflows/openapi-lint.yml) (issue #36, PR #37)
  - CI/CD and reporting API notes: [`docs/ci_cd_and_cost_reporting_api.md`](docs/ci_cd_and_cost_reporting_api.md) (issue #67, PR #68)
  - Docker Compose skeleton: [`docker-compose.yml`](docker-compose.yml) (issue #133, PR #134)
  - `sprint-1` release tag
  - Reporting and platform stories US-33–US-37, US-46–US-48, US-52: #103–#106, #121–#125
- **Pull requests opened:** #1–#7, #10, #12, #14, #37, #68, #110, #134
- **Commits:** [list](https://github.com/denizalponiki/Fleet-Tracking-System/commits/develop?author=denizalponiki)
- **Issues:** [opened](https://github.com/denizalponiki/Fleet-Tracking-System/issues?q=is%3Aissue+author%3Adenizalponiki) · [assigned](https://github.com/denizalponiki/Fleet-Tracking-System/issues?q=is%3Aissue+assignee%3Adenizalponiki)

## 6. Ahmet Tarık Orhan · Implementation & Integration Engineer (Backend & API)

- **Student no.:** 260201305 · **GitHub:** [@ahmettarikorhan](https://github.com/ahmettarikorhan)
- **Responsibilities:** reservation and carpool sections of the OpenAPI contract, Prism mock for the frontend, backend integration; code modules `reservation` and `carpool`.
- **Sprint 1 work:**
  - Reservation and carpool API notes with the Prism mock: [`docs/carpool_reservation_api.md`](docs/carpool_reservation_api.md) (issue #53, PR #54)
  - Aligned the reservation notes with the 409 maintenance code (issue #107, PR #108)
  - Contract consistency finding #52
  - Reservation and ride-sharing stories US-18–US-25: #55–#62
  - Reviewed and merged #136, #137
- **Pull requests opened:** #54, #108
- **Commits:** [list](https://github.com/denizalponiki/Fleet-Tracking-System/commits/develop?author=ahmettarikorhan)
- **Issues:** [opened](https://github.com/denizalponiki/Fleet-Tracking-System/issues?q=is%3Aissue+author%3Aahmettarikorhan) · [assigned](https://github.com/denizalponiki/Fleet-Tracking-System/issues?q=is%3Aissue+assignee%3Aahmettarikorhan)

## 7. Mustafa Düşünceli · Implementation & Integration Engineer (Frontend & UI)

- **Student no.:** 260204319 · **GitHub:** [@mustafadusunceli](https://github.com/mustafadusunceli)
- **Responsibilities:** screen list, user flows and Figma prototypes, consumer review of the OpenAPI contract, frontend implementation; code module `frontend`.
- **Sprint 1 work:**
  - UI/UX flow and screen list: [`docs/ui_ux_flow_and_dashboard.md`](docs/ui_ux_flow_and_dashboard.md) (issue #39, PR #109)
  - User interface stories US-38–US-45: #111–#118
  - Reviewed and merged #37
- **Pull requests opened:** #109
- **Commits:** [list](https://github.com/denizalponiki/Fleet-Tracking-System/commits/develop?author=mustafadusunceli)
- **Issues:** [opened](https://github.com/denizalponiki/Fleet-Tracking-System/issues?q=is%3Aissue+author%3Amustafadusunceli) · [assigned](https://github.com/denizalponiki/Fleet-Tracking-System/issues?q=is%3Aissue+assignee%3Amustafadusunceli)
