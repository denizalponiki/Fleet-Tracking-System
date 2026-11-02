---
name: User Story
about: A backlog item from docs/product_backlog.md (one story = one issue)
title: "[US-xx] "
labels: story
assignees: ''
---

<!-- Title format: [US-20] Reserve a vehicle for a trip  (same ID as in docs/product_backlog.md) -->

## Story
As a **<role: staff member / fleet manager / maintenance officer>**,
I want **<capability>**,
so that **<value>**.

## Acceptance Criteria
<!-- Copy from docs/product_backlog.md. Each criterion becomes at least one test case. -->
- **AC1** · Given … When … Then …
- **AC2** · Given … When … Then …

## Details
| | |
|---|---|
| Epic | E? · <epic name> |
| Module | `identity` / `vehicle` / `reservation` / `carpool` / `handover` / `maintenance` / `fuel` / `reporting` / `frontend` |
| Story points | 1 / 2 / 3 / 5 / 8 |
| Priority (MoSCoW) | Must / Should / Could |
| Target sprint | Sprint 2 / Sprint 3 / Final |
| Depends on | #<issue> |
| API endpoints | e.g. `POST /reservations/{reservationId}/pickup` |

## Definition of Ready
- [ ] Owner assigned and story points estimated
- [ ] Acceptance criteria are testable (Given / When / Then)
- [ ] Endpoints exist in `docs/openapi.yaml`
- [ ] Dependencies are done or planned in the same sprint

## Definition of Done
- [ ] Code merged into `develop` through a reviewed PR (merge commit, no squash)
- [ ] Unit tests written, CI green
- [ ] Every acceptance criterion verified by a test
- [ ] `docs/openapi.yaml` still matches the implementation
- [ ] Diagrams updated if the structure changed
