# FleetSync · Sprint 2 Plan and Report · Requirements and Design

> SENG 321 · Team 3 · Weeks 3–5 · Tag: `sprint-2` · Weight: 20%
> Owner: Mehmet Umut Oğuzcan (Scrum Master). Related: [`../raci_matrix.md`](../raci_matrix.md) · [`../git_flow.md`](../git_flow.md) · [`impediment_log.md`](impediment_log.md)
> Planned on 2026-11-21. Submission on Teams: 2026-11-24.

## 1. Sprint goal

Turn the Sprint 1 foundation into a complete requirements and design baseline, so that Sprint 3 can start coding the MVP without open design questions: SRS and refined backlog, measurable NFRs, Figma prototypes with user flows, and the C4 + UML architecture document, with OpenAPI frozen as v1.0.

## 2. Starting point

- Sprint 1 delivered and tagged (`sprint-1`); `main` and `develop` in sync after PR #235.
- Backlog: 10 epics, 23 features, user stories with acceptance criteria and story points; 58 task issues so far (Ali Eren 25, Abdullah 25, Mehmet Umut 8).
- No repository activity between 2026-11-06 and 2026-11-21 → the sprint runs compressed (see §3 and IMP-06).

## 3. Timeline

| Day | Date | Goal |
|---|---|---|
| D0 | 2026-11-21 (Sat) | Sprint 2 planning (WhatsApp, all members). Work starts today; issues opened under the `Sprint 2` milestone. |
| D1 | 2026-11-22 (Sun) | Stand-up (async). Every deliverable has a first draft as a PR against `develop`. |
| D2 | 2026-11-23 (Mon) | Stand-up (async). Cross-reviews (§6) and fixes; OpenAPI v1.0 frozen; all PRs merged by the evening. |
| D3 | 2026-11-24 (Tue) | `develop` → `main`, tag `sprint-2`, submission ZIP, submission on Teams. |

## 4. Sprint 2 deliverables (specification)

| # | Deliverable | Owner (A/R) | Contributors | Output in the repository | Done when |
|---|---|---|---|---|---|
| 1 | Detailed SRS and refined backlog | Ahmet Can Vurmaz | Ali Eren Kurt (use case diagram), Abdullah Tecimen (testability) | `docs/srs.md`; updated `docs/product_backlog.md`; `Sprint 2` / `Sprint 3` milestones on the issues | Functional requirements traced to stories; use case diagram; traceability matrix story → endpoint → test → PR; Sprint 3 scope (MoSCoW) fixed |
| 2 | Non-functional requirements and quality measures | Abdullah Tecimen | Deniz Alp Oniki (deploy and operations NFRs), Ali Eren Kurt | `docs/nfr_quality.md`; test case catalogue update in `docs/test_plans_and_coverage.md` | Every NFR has a measurable target and a measurement method (performance, security, usability, reliability, maintainability, coverage ≥ 50%) |
| 3 | Figma UI/UX prototypes and user-flow diagrams | Mustafa Düşünceli | Mehmet Umut Oğuzcan (checklist screens review), Ahmet Can Vurmaz (stories) | Public Figma link + screenshots and user-flow diagrams in `docs/ui_ux_flow_and_dashboard.md` | Flows for trip request, pickup/return and maintenance alert; every screen linked to a story (US-38–US-45) |
| 4 | C4 and UML architecture document | Ali Eren Kurt | Ahmet Tarık Orhan (sequence diagram, reservation tables), Deniz Alp Oniki (deployment diagram), Ahmet Can Vurmaz (use case) | `docs/architecture.md` (+ `docs/diagrams/`) | C4 L2 and L3; class, sequence (demo journey), state (vehicle, reservation), deployment, ER; component names match package names |
| 5 | OpenAPI v1.0 freeze | Ali Eren Kurt | Ahmet Tarık Orhan, Mustafa Düşünceli (consumer review) | `docs/openapi.yaml` `info.version: 1.0.0`, tag `openapi-v1.0` | Lint passes; later changes only by PR with Architect approval |

## 5. Role tasks

| Member | Sprint 2 tasks |
|---|---|
| Ahmet Can Vurmaz | SRS, refined backlog with MoSCoW and Sprint 3 scope, use case diagram (with Ali Eren), traceability matrix |
| Mehmet Umut Oğuzcan | Sprint 1 retrospective, stand-up records, this report, impediment log, `Sprint 2` milestone and board, review of the checklist screens in Figma, `TripCompletedEvent` contract (with Ali Eren), submission ZIP and evidence, `CONTRIBUTIONS.md` update |
| Ali Eren Kurt | Architecture document (C4 L2/L3, UML set, ER), ADRs for new decisions, OpenAPI v1.0 freeze |
| Abdullah Tecimen | NFR and quality measures, test case catalogue for the Sprint 3 Must stories, close findings F1–F5 |
| Deniz Alp Oniki | Deploy and operations NFRs, deployment diagram input, seed data design, CI test + coverage step (stretch) |
| Ahmet Tarık Orhan | Sequence diagram input for the demo journey, reservation tables for the ER diagram, OpenAPI v1.0 review of reservation and carpool paths |
| Mustafa Düşünceli | Figma prototypes, user-flow diagrams, screen ↔ story mapping |

Stretch, only if the deliverables above are done (code officially starts in Sprint 3): Flyway `V1__init.sql`, port interface stubs, maintenance rule engine with TDD, React skeleton against the Prism mock, CI unit tests with a coverage report.

Every member opens at least one issue and one PR under the `Sprint 2` milestone and reviews at least one PR from someone else. Members without task issues yet (Ahmet Can, Deniz, Ahmet Tarık, Mustafa) add tasks for their Sprint 3 stories during refinement.

## 6. Review pairs

| Deliverable | Reviewer | Checks |
|---|---|---|
| SRS + backlog | Abdullah Tecimen | Requirements are testable and traced |
| NFR | Deniz Alp Oniki | Targets are measurable and achievable in the stack |
| Figma | Mehmet Umut Oğuzcan, Ahmet Can Vurmaz | Each screen maps to a story; checklist screens match US-26–US-28 |
| Architecture | Ahmet Tarık Orhan | Diagrams match OpenAPI, package names and the ER schema |
| OpenAPI v1.0 | Mustafa Düşünceli | Frontend can build every screen from the contract |

## 7. Definition of Done for Sprint 2

- Merged into `develop` through a reviewed PR (merge commit), then into `main` before the tag.
- Diagrams render on GitHub (Mermaid) or are committed as images with their source.
- Names are consistent across SRS, OpenAPI, diagrams and backlog (actors, modules, statuses, error codes).
- Each document starts with owner, version and date.

## 8. Meetings

| Meeting | When | Where |
|---|---|---|
| Sprint 2 planning | 2026-11-21 | WhatsApp |
| Sprint 1 retrospective | 2026-11-21–22 (async) | WhatsApp |
| Stand-up | 2026-11-22, 2026-11-23 (async) | WhatsApp |
| Sprint 2 review + retrospective | After the submission | Micup |

### Stand-up records

### Planning meeting · 2026-11-21 (WhatsApp)
Present: all seven members · Absent: none
Each member presented their Sprint 2 tasks; the distribution in §4 and §5 was accepted. Decision: work starts on 2026-11-21 because the submission is on 2026-11-24.

| Member | Sprint 2 task presented | Blocker |
|---|---|---|
| Ahmet Can Vurmaz | SRS, refined backlog, use case diagram, traceability matrix | – |
| Mehmet Umut Oğuzcan | Retrospective, stand-ups, sprint report, Figma checklist review, `TripCompletedEvent` contract, submission | – |
| Ali Eren Kurt | C4 and UML architecture document, ER, OpenAPI v1.0 freeze | – |
| Abdullah Tecimen | NFR and quality measures, test case catalogue | – |
| Deniz Alp Oniki | Deploy and operations NFRs, deployment diagram input, seed data design | – |
| Ahmet Tarık Orhan | Sequence diagram input, reservation tables, OpenAPI v1.0 review | – |
| Mustafa Düşünceli | Figma prototypes and user-flow diagrams | – |

### Stand-up · 2026-11-22 (async, WhatsApp)
Present: all seven members · Absent: none

| Member | Done (2026-11-21 and today) | Next | Blocker |
|---|---|---|---|
| Ahmet Can Vurmaz | Backlog corrections (US-11, US-12, US-31, F1–F5 decisions); detailed SRS (`srs/srs.md`) and traceability matrix as PRs; licence renewal rule (#262) and Abdullah's F3–F5 questions (carbon, working hours, fuel anomaly) settled and written into the documents | Link the use case diagram from the SRS (PR #294); follow his open PRs to merge; update the traceability matrix with any new test IDs before the `main` merge | None; waiting for reviews and merges |
| Mehmet Umut Oğuzcan | Sprint 2 plan, IMP-06 and milestone (#257); Sprint 1 retrospective (#261); `TripCompletedEvent` contract agreed with the Architect, `trip_completed_event.md` merged into `domain_events.md`, C4 and UML links updated (#270); review of the handover screens S6–S8 on #292; approvals on #289 and #291; review and merge of #294 | Follow #289 and #291 to merge; final sprint report and `CONTRIBUTIONS.md` update | None; #289 and #291 wait for the code-owner review |
| Ali Eren Kurt | C4, UML, ER and use case diagrams; ADR-002 to ADR-005 and other architecture decisions; API contract frozen as v1.0.0; backend skeleton for Sprint 3; reviewed issues and PRs that needed his approval | PR approvals | None |
| Abdullah Tecimen | Edited the files that needed changes; settled the open decisions with teammates and updated the documents | Available to help teammates on request | None |
| Deniz Alp Oniki | Deployment architecture review and demo seed data design (#283, #285 merged); reporting requirements and operational NFRs; review of the QA test cases; approved #289; requested changes on #291 for two technical inconsistencies; closed #282 and #284 | Track the open PRs before the release | Waiting for the fixes on #291 and the remaining Sprint 2 merges |
| Ahmet Tarık Orhan | Closed the Sprint 2 reviews: approved #245, #249, #274, #278; reservation, carpool and performance input on #160, #161, #162, #237, #246 | Review #289 and #291; open one issue and one PR to bring `carpool_reservation_api.md` to Sprint 2 and mark his performance row in the NFR as Confirmed | None |
| Mustafa Düşünceli | Issue #255; Figma file and shared components; Staff (8), Maintenance Officer (3) and Fleet Manager (3) screens; US-44 fuel receipt screen (15 screens in total); clickable prototype; contrast fixed against NFR-ACC-01; `ui_ux_flow_and_dashboard.md` v0.2 (Figma link, screen–story mapping, four user flows, screenshots) in PR #292; frontend review and approval of #289 | Apply the review comments on #292; merge after approval | #292 waited for the code-owner review of Ali Eren (later merged with the review fixes) |

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

## 9. Sprint 1 retrospective

Collected asynchronously on WhatsApp, 2026-11-21.

| Went well | To improve | Action for Sprint 2 (owner) |
|---|---|---|
| Teamwork, and setting up the basic architecture went smoothly | – | Keep the role split and the review pairs in §6 (all) |
| – | Periods without communication in the team | Async stand-ups on WhatsApp on 2026-11-22 and 2026-11-23 (Mehmet Umut Oğuzcan) |
| – | Little experience with architecture design | Architecture drafts reviewed early by a second member before the final PR (Ali Eren Kurt, Ahmet Tarık Orhan) |
| – | Problems were found late, and each finding became a separate issue, which inflated the issue list | Check each other's work early, while it is still a draft PR; group small findings into one review comment or one issue per document (all) |

## 10. Risks

| Risk | Impact | Response |
|---|---|---|
| Compressed sprint (four days) after two inactive weeks | Deliverables incomplete at submission | Drafts as PRs by 2026-11-22, reviews and merges on 2026-11-23; stretch items dropped first |
| Documents disagree (names, statuses, codes) | Architecture and requirements scores drop | Review pairs (§6) check cross-document consistency |
| Low activity of some members | Individual contribution grades drop | Every member owns at least one PR and one review this sprint |
| Figma link not reachable by the assistants | Prototype not gradable | Public view link + screenshots in the repository |

## 11. Sprint backlog status

| Deliverable | Owner | Issue | PR | Status |
|---|---|---|---|---|
| SRS and refined backlog | Ahmet Can Vurmaz | | | Not started |
| NFR and quality measures | Abdullah Tecimen | | | Not started |
| Figma prototypes and user flows | Mustafa Düşünceli | | | Not started |
| C4 and UML architecture document | Ali Eren Kurt | | | Not started |
| OpenAPI v1.0 freeze | Ali Eren Kurt | | | Not started |
| `TripCompletedEvent` contract | Mehmet Umut Oğuzcan, Ali Eren Kurt | | | Not started |
| Sprint 1 retrospective, stand-ups, this report | Mehmet Umut Oğuzcan | #251 | #257 | In progress |
| `develop` → `main` and `sprint-2` tag | Deniz Alp Oniki | | | Not started |

## 12. Submission checklist

- [ ] All five items in §4 merged into `main`
- [ ] `sprint-2` tag on `main`
- [ ] `CONTRIBUTIONS.md` updated with Sprint 2 work
- [ ] Figma link opens without signing in
- [ ] ZIP with all Sprint 2 documents uploaded on Teams with the repository link
