# FleetSync – Test Plan and Coverage Strategy

| | |
|---|---|
| Course | SENG 321 Software Engineering · Sprint 1 |
| Owner | Abdullah Tecimen – Quality Assurance & Test Automation Engineer |
| Version | 0.3 · Sprint 1 (aligned with the revised `openapi.yaml` of 2026-11-02) |
| Related documents | [`product_backlog.md`](product_backlog.md), [`openapi.yaml`](openapi.yaml), [`system_vision.md`](system_vision.md), [`raci_matrix.md`](raci_matrix.md) |

---

## 1. Purpose

This document defines how FleetSync is tested throughout the semester: test levels, tools, quality targets, the defect-tracking process and the catalogue of critical test cases. Every test case is derived from an acceptance criterion in `product_backlog.md` and uses the exact status values and error codes defined in `openapi.yaml`, so that tests, requirements and the API contract stay consistent.

## 2. Quality Targets

| Metric | Target | Deadline |
|--------|--------|----------|
| Unit-test coverage (backend) | ≥ 50% | Sprint 3 (Week 8) |
| CI pipeline | All tests run automatically on every PR to `develop` | Sprint 3 |
| Must stories with at least one automated test per acceptance criterion | 100% | Final (Week 10) |
| Critical / blocker defects open at demo | 0 | Final (Week 10) |
| SonarQube quality gate | Passed, no critical issues | Final (Week 10) |
| Jury demo journey | Covered by an automated E2E test | Final (Week 10) |

## 3. Test Levels

| Level | What is tested | Responsibility |
|-------|----------------|----------------|
| Unit | Single functions and classes (e.g. maintenance threshold calculation, reservation overlap check, consumption calculation) | Each module owner writes unit tests for their own module; QA reviews them and monitors coverage. Tests of the `fuel` module are reviewed by another member. |
| Integration | API, services and PostgreSQL together (e.g. a reservation request is stored and an overlapping one is rejected) | QA with the Backend Engineer |
| End-to-End | Complete user journeys through the UI and API | QA with the Frontend Engineer |

## 4. Tools

Technology stack: Python (FastAPI) backend, React (Vite + Tailwind CSS) frontend, PostgreSQL database.

| Purpose | Tool |
|---------|------|
| Backend unit tests | pytest |
| Coverage measurement | pytest-cov |
| API / integration tests | FastAPI TestClient (httpx) with a PostgreSQL test database in Docker (Testcontainers for Python) |
| API contract check | OpenAPI lint in CI (owned by DevOps); responses checked against `openapi.yaml` schemas |
| Frontend unit tests | Vitest + React Testing Library |
| End-to-end tests | Playwright (Python) |
| Static analysis | SonarQube (owned by DevOps) |
| CI execution | GitHub Actions – tests and coverage run on every PR to `develop` |

Integration tests use PostgreSQL, not SQLite, because date-time and constraint behaviour differs between the two and reservation-conflict tests depend on it.

## 5. Naming Conventions Used in Test Cases

To keep tests consistent with the API contract, expected results use only the values defined in `openapi.yaml`:

| Concept | Values (from `openapi.yaml`) |
|---|---|
| Vehicle status | `AVAILABLE`, `IN_USE`, `IN_MAINTENANCE`, `OUT_OF_SERVICE` |
| Reservation status | `CONFIRMED`, `ACTIVE`, `COMPLETED`, `CANCELLED` |
| Maintenance rule evaluation | `OK`, `DUE_SOON`, `DUE` |
| Maintenance alert | level `DUE_SOON` / `DUE`, status `OPEN` / `RESOLVED` |
| Recommendation block reasons | `MAINTENANCE_DUE`, `MAINTENANCE_DUE_SOON`, `INSUFFICIENT_SEATS`, `CALENDAR_CONFLICT`, `LICENSE_EXPIRED`, `LICENSE_CLASS_MISMATCH`, `VEHICLE_NOT_AVAILABLE` |
| Fuel anomaly types | `CONSUMPTION_SPIKE`, `OUTSIDE_RESERVATION` |
| Error responses | `application/problem+json` with HTTP status and a `code` field, e.g. `409 RESERVATION_CONFLICT` |

## 6. Critical Test Case Catalogue

Each test case names the user story it verifies (`US-xx` in `product_backlog.md`) and the business rule it comes from (`system_vision.md` §8). Level: **U** = unit, **I** = integration, **E** = end-to-end.

### 6.1 Predictive Maintenance (mileage and date rules)

Boundary-value tests around the oil change rule (interval 10,000 km, warning threshold 1,000 km).

| ID | User story | Scenario | Expected result | Level |
|----|-----------|----------|-----------------|-------|
| TC-MNT-01 | US-11 | Last oil change at 0 km, odometer 8,999 km | Oil change rule `OK`, 1,001 km remaining | U |
| TC-MNT-02 | US-11 | Last oil change at 0 km, odometer 9,000 km | Oil change rule `DUE_SOON` | U |
| TC-MNT-03 | US-11 | Last oil change at 0 km, odometer 10,000 km | Oil change rule `DUE` | U |
| TC-MNT-04 | US-11 | Inspection due date is 30 days away | Inspection rule `DUE_SOON` | U |
| TC-MNT-05 | US-13 | Vehicle returned with odometer 9,999 km | No `DUE` alert; vehicle `AVAILABLE` | U, I |
| TC-MNT-06 | US-13 | Vehicle returned with odometer 10,000 km | Alert level `DUE`, status `OPEN` ("10,000 km service is due"); vehicle `IN_MAINTENANCE` | U, I |
| TC-MNT-07 | US-13 | Vehicle returned with odometer 10,050 km | Alert raised; vehicle `IN_MAINTENANCE` | U, I |
| TC-MNT-08 | US-15 | Officer records the oil change for an `IN_MAINTENANCE` vehicle | Alert `RESOLVED`; interval restarts; vehicle `AVAILABLE` | I |
| TC-MNT-09 | US-15 | Service recorded with odometer lower than the vehicle's odometer | `422` (mileage lower than recorded) | I |
| TC-MNT-10 | US-09 | Manager sets an `IN_MAINTENANCE` vehicle to `AVAILABLE` manually | `409 INVALID_STATUS_TRANSITION` | I |

### 6.2 Trip Blocking and Vehicle Recommendation

Rule: a vehicle is blocked when remaining km < estimated trip km + 100 km safety buffer.

| ID | User story | Scenario | Expected result | Level |
|----|-----------|----------|-----------------|-------|
| TC-REC-01 | US-12 | 350 km remaining, 300 km trip | Blocked (350 < 400), reason `MAINTENANCE_DUE_SOON` | U |
| TC-REC-02 | US-12 | 400 km remaining, 300 km trip | Not blocked (400 is not below 400) | U |
| TC-REC-03 | US-12 | Inspection due date falls before the trip ends | Blocked, reason `MAINTENANCE_DUE_SOON` | U |
| TC-REC-04 | US-19 | Vehicle has fewer seats than requested | Listed as blocked, reason `INSUFFICIENT_SEATS` | U, I |
| TC-REC-05 | US-19 | Vehicle already reserved in the requested period | Listed as blocked, reason `CALENDAR_CONFLICT` | I |
| TC-REC-06 | US-19 | One vehicle near service and one suitable vehicle (demo seed data) | Suitable vehicle recommended; the other blocked with its reason | I, E |

### 6.3 Reservations and Conflicts

| ID | User story | Scenario | Expected result | Level |
|----|-----------|----------|-----------------|-------|
| TC-RES-01 | US-20 | Reserve a free, safe vehicle with an eligible driver | `201`; reservation `CONFIRMED` | I |
| TC-RES-02 | US-20 | Overlapping period on the same vehicle (10:00–12:00 vs 11:00–13:00) | `409 RESERVATION_CONFLICT` | U, I |
| TC-RES-03 | US-20 | Back-to-back period (10:00–12:00 vs 12:00–14:00) | `201` (no overlap) | U, I |
| TC-RES-04 | US-20 | Vehicle blocked for maintenance reserved directly through the API | `409 VEHICLE_MAINTENANCE_DUE` | I |
| TC-RES-05 | US-20 | End time before start time, or more than 14 days after it | `400 VALIDATION_ERROR` | I |
| TC-RES-06 | US-22 | Cancel an `ACTIVE` reservation | `409 RESERVATION_NOT_CANCELLABLE` | I |
| TC-RES-07 | US-21 | Staff member opens another user's reservation | `403 FORBIDDEN` | I |
| TC-RES-08 | US-20 | Vehicle that is `IN_MAINTENANCE` or `OUT_OF_SERVICE` reserved directly through the API | `409 VEHICLE_UNAVAILABLE` | I |
| TC-RES-09 | US-20 | Driver's licence expires before the trip ends | `422 LICENSE_EXPIRED` | I |
| TC-RES-10 | US-20 | Vehicle with fewer seats than requested reserved directly through the API | `422 SEAT_CAPACITY_EXCEEDED` | I |

### 6.4 Driver Eligibility

| ID | User story | Scenario | Expected result | Level |
|----|-----------|----------|-----------------|-------|
| TC-ELG-01 | US-05 | Verified licence of the required class, valid after the trip ends | Eligible | U |
| TC-ELG-02 | US-05 | Licence expires before the trip ends | Not eligible, reason `LICENSE_EXPIRED` | U |
| TC-ELG-03 | US-05 | Licence class does not allow the vehicle | Not eligible, reason `LICENSE_CLASS_MISMATCH` | U |
| TC-ELG-04 | US-05 | Licence not yet verified | Not eligible | U |
| TC-ELG-05 | US-04 | Staff member tries to verify a licence | `403 FORBIDDEN` | I |

### 6.5 Handover and Mileage Limits

Rule: odometer readings never go backwards; a trip more than 30% longer than estimated is flagged.

| ID | User story | Scenario | Expected result | Level |
|----|-----------|----------|-----------------|-------|
| TC-HND-01 | US-26 | Pickup with complete checklist | Reservation `ACTIVE`; vehicle `IN_USE` | I |
| TC-HND-02 | US-26 | Pickup checklist missing a required item | `422 CHECKLIST_INCOMPLETE` | I |
| TC-HND-03 | US-27 | Return odometer lower than pickup odometer | `422 ODOMETER_DECREASED` | U, I |
| TC-HND-04 | US-27 | Estimated 100 km, actual trip 130 km | `kmLimitExceeded = false` | U |
| TC-HND-05 | US-27 | Estimated 100 km, actual trip 131 km | `kmLimitExceeded = true` | U |
| TC-HND-06 | US-27 | Valid return | Reservation `COMPLETED`; `tripKm` = return − pickup odometer | I |

### 6.6 Fuel Receipts and Anomalies

Rule: consumption more than 25% above the vehicle's average, or litres above tank capacity, is flagged.

| ID | User story | Scenario | Expected result | Level |
|----|-----------|----------|-----------------|-------|
| TC-FUEL-01 | US-29 | Valid receipt for an existing vehicle | `201`; unit price calculated | U, I |
| TC-FUEL-02 | US-29 | Litres or total price of 0 or below | `400 VALIDATION_ERROR` | I |
| TC-FUEL-03 | US-29 | Litres above the vehicle's tank capacity | `422 FUEL_EXCEEDS_TANK` | U, I |
| TC-FUEL-04 | US-29 | Receipt for a non-existent vehicle | `404 NOT_FOUND` | I |
| TC-FUEL-05 | US-30 | Two full-tank receipts 500 km apart, 40 L at the second | Consumption 8.0 L/100 km | U |
| TC-FUEL-06 | US-31 | Average 8.0 L/100 km, new value 10.1 L/100 km (> 25%) | Receipt saved, anomaly `CONSUMPTION_SPIKE` | U |
| TC-FUEL-07 | US-31 | Average 8.0 L/100 km, new value exactly 10.0 L/100 km (25%) | Not flagged | U |
| TC-FUEL-08 | US-31 | Receipt dated outside any reservation of the vehicle | Anomaly `OUTSIDE_RESERVATION` | U |
| TC-FUEL-09 | US-31 | Staff member requests the anomaly list | `403 FORBIDDEN` | I |

### 6.7 Ride Sharing

Rule: same destination, departure within 30 minutes, enough free seats.

| ID | User story | Scenario | Expected result | Level |
|----|-----------|----------|-----------------|-------|
| TC-POOL-01 | US-23 | Same destination, departure 30 minutes later, free seat | Ride returned as a match | U |
| TC-POOL-02 | US-23 | Same destination, departure 31 minutes later | Not matched | U |
| TC-POOL-03 | US-23 | No free seats, or ride sharing disabled by the driver | Not matched | U |
| TC-POOL-04 | US-24 | Join a ride with a free seat | `201`; free seats decrease by one | I |
| TC-POOL-05 | US-24 | Join a full ride | `422 SEAT_CAPACITY_EXCEEDED` | I |
| TC-POOL-06 | US-24 | Join a ride already joined | `409 ALREADY_JOINED` | I |

### 6.8 Authentication and Authorisation

| ID | User story | Scenario | Expected result | Level |
|----|-----------|----------|-----------------|-------|
| TC-AUTH-01 | US-01 | Correct email and password | `200`; JWT and role returned | I |
| TC-AUTH-02 | US-01 | Wrong password | `401 INVALID_CREDENTIALS` | I |
| TC-AUTH-03 | US-01 | Any endpoint except login without a token | `401 UNAUTHORIZED` | I |
| TC-AUTH-04 | US-02 | Create a user with an existing email | `409 DUPLICATE_EMAIL` | I |

### 6.9 Jury Demo Journey (E2E)

| ID | User stories | Scenario (`system_vision.md` §11) | Expected result | Level |
|----|-------------|-----------------------------------|-----------------|-------|
| TC-E2E-01 | US-40, US-19, US-12, US-20 | Staff member requests a vehicle; the vehicle near service is shown as blocked with its reason; a suitable vehicle is reserved | Blocked vehicle and reason visible; reservation `CONFIRMED` | E |
| TC-E2E-02 | US-41, US-24 | A colleague joins the ride | Passenger added; free seats decrease | E |
| TC-E2E-03 | US-42, US-26, US-27, US-13 | Pickup with checklist; return with mileage crossing 10,000 km | "10,000 km service is due" shown; vehicle `IN_MAINTENANCE` | E |
| TC-E2E-04 | US-43, US-15 | Maintenance officer sees the alert and records the service | Alert `RESOLVED`; vehicle `AVAILABLE` | E |
| TC-E2E-05 | US-45, US-34–36 | Fleet manager opens reports for the period | Cost, carbon and utilisation shown | E |

## 7. Traceability: Must Stories and Their Test Cases

| User story | Test cases |
|---|---|
| US-01, US-02 | TC-AUTH-01 – TC-AUTH-04 |
| US-04, US-05 | TC-ELG-01 – TC-ELG-05 |
| US-11 | TC-MNT-01 – TC-MNT-04 |
| US-12 | TC-REC-01 – TC-REC-03 |
| US-13 | TC-MNT-05 – TC-MNT-07, TC-E2E-03 |
| US-15 | TC-MNT-08, TC-MNT-09, TC-E2E-04 |
| US-19 | TC-REC-04 – TC-REC-06, TC-E2E-01 |
| US-20, US-21 | TC-RES-01 – TC-RES-05, TC-RES-07 – TC-RES-10, TC-E2E-01 |
| US-23, US-24 | TC-POOL-01 – TC-POOL-06, TC-E2E-02 |
| US-26, US-27 | TC-HND-01 – TC-HND-06, TC-E2E-03 |
| US-29 | TC-FUEL-01 – TC-FUEL-04 |
| US-34 – US-36, US-45 | TC-E2E-05 (detailed report tests added in Sprint 2) |
| US-38 – US-43 | TC-E2E-01 – TC-E2E-05 |
| US-46 – US-51 | Verified by the CI pipeline itself (build, coverage report, E2E run) |

Must stories that are not listed yet (US-03, US-07, US-08, US-14, US-18) get their test cases during Sprint 2 together with the SRS.

## 8. Acceptance Criteria Review (Sprint 1)

QA reviewed all acceptance criteria in `product_backlog.md` for testability and compared them with `system_vision.md` and `openapi.yaml`.

| # | Finding | Affected | Status |
|---|---|---|---|
| F1 | Demo step 5 says the maintenance officer is notified, but `openapi.yaml` has no notification endpoint. Tests assume the notification is the `OPEN` alert in `GET /maintenance/alerts` plus a UI indicator. | US-13, US-43 | Open – decision by PO and Architect |
| F2 | CSV export is listed in `system_vision.md` §7.1 but has no endpoint in `openapi.yaml`. | US-37 | Open |
| F3 | The CO₂ factor per litre is not defined, so the carbon report cannot be checked against an expected value. | US-35 | Open |
| F4 | "Available working hours" for utilisation is not defined. | US-36 | Open |
| F5 | The number of earlier full-tank intervals needed before a fuel average is used is not defined. | US-31 | Open |
| F6 | `POST /reservations` returns several error codes under the same HTTP status: 409 for vehicle problems (`RESERVATION_CONFLICT`, `VEHICLE_MAINTENANCE_DUE`, `VEHICLE_UNAVAILABLE`) and 422 for driver or request problems (`LICENSE_EXPIRED`, `LICENSE_CLASS_MISMATCH`, `SEAT_CAPACITY_EXCEEDED`). Tests check the `code` field, not only the HTTP status. | US-20 | Applied in this plan |
| F8 | The revised `openapi.yaml` (2026-11-02) returns `409 VEHICLE_MAINTENANCE_DUE` when a blocked vehicle is reserved; test plan v0.2 and `product_backlog.md` US-20 criterion 4 still said 422. Reported by the Backend Engineer in `carpool_reservation_api.md`. Test plan fixed in v0.3; backlog to be updated by the Product Owner. | US-20 | Test plan fixed; backlog open |
| F7 | Test plan v0.1 used `MAINTENANCE` as a vehicle status and generic HTTP names; aligned with `IN_MAINTENANCE` and the API error codes in v0.2. | Test plan | Fixed |

All other acceptance criteria are measurable and have explicit boundary values.

## 9. Defect Tracking Process

1. Defects are reported as GitHub Issues with the **Bug Report** template.
2. Each defect gets the `bug` label, a severity and the related user story ID.
3. The defect is assigned to the owner of the related module.
4. The fix is delivered through a PR that references the issue (`Closes #<id>`).
5. QA verifies the fix with a test and confirms the issue is closed.

Findings from document reviews (section 8) are tracked as issues with the `qa-review` label.

## 10. Entry and Exit Criteria

**A story is ready for testing when** it is merged into `develop` and its acceptance criteria are defined in the backlog.

**A story is done when** its tests pass in CI, every acceptance criterion is verified by at least one test, and it has no open critical or major defects (see the Definition of Done in `product_backlog.md`).

## 11. Quality Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Unit-test coverage stays below 50% | Sprint 3 grade loss | Tests required in the PR checklist; coverage reported in CI |
| Modules work alone but fail when integrated | Broken MVP | Integration tests against PostgreSQL |
| Main demo flow fails in front of the jury | Demo grade loss | Automated E2E test for the demo journey; fixed seed data; rehearsal |
| Code and API contract drift apart | Frontend and backend integration fails | Tests use the codes in `openapi.yaml`; contract checked in CI |

## 12. Submission Checklist (QA check before each delivery)

Before each sprint submission, QA checks:

- [ ] Every required deliverable file exists in `docs/` on `develop` and the links between documents work.
- [ ] `openapi.yaml` validates without errors.
- [ ] Status values and error codes are identical in the backlog, the test plan and `openapi.yaml`.
- [ ] Every Must story has at least one test case.
- [ ] Every team member has commits, pull requests or reviews in the sprint.
- [ ] All pull requests for the sprint are merged into `develop`; no open PR is needed for the submission.
- [ ] `develop` is merged into `main` and the sprint release tag is created on `main`.
- [ ] Links to issues, pull requests, commits and the release tag are listed in the submission document.

## 13. Planned Updates

- **Sprint 2:** Test cases for the remaining Must stories; non-functional quality measures; close findings F1–F5.
- **Sprint 3:** Coverage report from the CI pipeline; unit and integration tests implemented.
- **Final:** Integration and E2E test report; SonarQube summary.
