# FleetSync – Test Plan and Coverage Strategy

**Owner:** Abdullah Tecimen – Quality Assurance & Test Automation Engineer
**Version:** 0.1 (Sprint 1 – Initial Draft)
**Status:** Draft – will be detailed in Sprint 2 together with the SRS

---

## 1. Purpose

This document defines how FleetSync will be tested throughout the semester. It describes the test levels, tools, quality targets, defect-tracking process and the initial set of critical test scenarios derived from the project scope and the jury demo scenario.

## 2. Quality Targets

| Metric | Target | Deadline |
|--------|--------|----------|
| Unit-test coverage | ≥ 50% | Sprint 3 (Week 8) |
| CI pipeline | All tests run automatically on every PR to `develop` | Sprint 3 |
| Critical / blocker defects open at demo | 0 | Final (Week 10) |
| SonarQube quality gate | Passed, no critical issues | Final (Week 10) |
| Demo user journey | Covered by an automated E2E test | Final (Week 10) |

## 3. Test Levels

| Level | What is tested | Responsibility |
|-------|----------------|----------------|
| Unit | Single functions and classes (e.g. maintenance rule calculation, reservation overlap check) | Each module owner writes unit tests for their own code; QA reviews and monitors coverage |
| Integration | Interaction between API, services and database (e.g. reservation endpoint writes to DB and rejects conflicts) | QA with Backend Engineer |
| End-to-End | Complete user journeys through the UI and API | QA with Frontend Engineer |

## 4. Tools

The final tool selection depends on the technology stack decided by the Lead Architect. Candidate tools:

| Purpose | Option (Java / Spring) | Option (Python) | Option (Node.js) |
|---------|------------------------|-----------------|------------------|
| Unit tests | JUnit 5 + Mockito | pytest | Jest |
| Coverage | JaCoCo | pytest-cov | Jest --coverage |
| API / integration | Spring Boot Test, REST Assured | pytest + TestClient | Supertest |
| E2E | Playwright | Playwright | Playwright / Cypress |
| Static analysis | SonarQube (shared with DevOps) | SonarQube | SonarQube |

## 5. Critical Test Areas

### 5.1 Predictive Maintenance (mileage and date rules)
Boundary-value testing around maintenance thresholds.

| ID | Scenario | Expected Result |
|----|----------|-----------------|
| TC-MNT-01 | Vehicle mileage since last service = 9,999 km | No maintenance alert |
| TC-MNT-02 | Vehicle mileage since last service = 10,000 km | "10,000 km service due" alert; status → `MAINTENANCE` |
| TC-MNT-03 | Vehicle mileage since last service = 10,050 km | Alert generated; status → `MAINTENANCE` |
| TC-MNT-04 | Inspection date has passed | Alert generated; vehicle cannot be reserved |
| TC-MNT-05 | Entered end mileage is lower than start mileage | Request rejected with validation error |

### 5.2 Vehicle Reservation and Conflicts

| ID | Scenario | Expected Result |
|----|----------|-----------------|
| TC-RES-01 | Reserve a free vehicle | Reservation created |
| TC-RES-02 | Overlapping time range (10:00–12:00 vs 11:00–13:00) | Rejected with `409 Conflict`, alternative vehicle suggested |
| TC-RES-03 | Back-to-back range (10:00–12:00 vs 12:00–14:00) | Accepted (no overlap) |
| TC-RES-04 | Vehicle with upcoming maintenance is requested | Vehicle blocked; suitable alternative suggested |
| TC-RES-05 | Driver with invalid or expired licence requests a vehicle | Request rejected |

### 5.3 Fuel Consumption and Anomalies

| ID | Scenario | Expected Result |
|----|----------|-----------------|
| TC-FUEL-01 | Valid fuel receipt is submitted | Receipt saved and linked to the vehicle |
| TC-FUEL-02 | Negative litres or negative amount | Rejected with `400 Bad Request` |
| TC-FUEL-03 | Consumption far above the vehicle's average | Receipt saved and flagged as anomaly |
| TC-FUEL-04 | Receipt for a non-existent vehicle | Rejected with `404 Not Found` |

### 5.4 Carpooling Matching

| ID | Scenario | Expected Result |
|----|----------|-----------------|
| TC-POOL-01 | Two staff members with same destination and overlapping time | Matched for shared ride |
| TC-POOL-02 | Same destination, non-overlapping time | Not matched |
| TC-POOL-03 | Vehicle capacity is full | No additional passengers matched |

### 5.5 Jury Demo Journey (E2E)

| ID | Scenario | Expected Result |
|----|----------|-----------------|
| TC-E2E-01 | Staff requests a vehicle → system blocks the vehicle with upcoming maintenance and suggests a suitable one → trip ends and new mileage is entered | System generates the "10,000 km service due" alert and moves the vehicle to maintenance status |

## 6. Defect Tracking Process

1. Defects are reported as GitHub Issues using the **Bug Report** template.
2. Each defect gets the `bug` label and a severity.
3. The defect is assigned to the owner of the related module.
4. The fix is delivered through a PR that references the issue (`Closes #<id>`).
5. QA verifies the fix and confirms the issue is closed.

## 7. Entry and Exit Criteria

**A feature is ready for testing when:** it is merged into `develop` and its acceptance criteria are defined in the backlog.

**A feature is done when:** its unit tests pass in CI, its acceptance criteria are verified, and it has no open critical or major defects.

## 8. Quality Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Unit-test coverage stays below 50% | Sprint 3 grade loss | Tests required in the PR checklist; coverage reported in CI |
| Modules work alone but fail when integrated | Broken MVP | Integration tests on API and database layers |
| Main demo flow fails in front of the jury | Demo grade loss | Automated E2E test for the demo journey; rehearsal before the demo |
| Acceptance criteria are not measurable | Untestable requirements | QA reviews user stories for testability during backlog refinement |

## 9. Planned Updates

- **Sprint 2:** Link test cases to user-story IDs from the SRS; finalize tools after stack decision; add non-functional quality measures.
- **Sprint 3:** Add coverage report from the CI pipeline.
- **Final:** Integration and E2E test report; SonarQube summary.
