# FleetSync – Test Plan and Coverage Strategy

| | |
|---|---|
| Course | SENG 321 Software Engineering · Sprint 2 |
| Owner | Abdullah Tecimen – Quality Assurance & Test Automation Engineer |
| Version | 0.6 · Sprint 2 (non-functional test cases from `nfr_quality_measures.md` §4 added; F1, F2, F9, F10 closed; F3–F5 decided) |
| Related documents | [`product_backlog.md`](product_backlog.md), [`openapi.yaml`](openapi.yaml), [`system_vision.md`](system_vision.md), [`raci_matrix.md`](raci_matrix.md), [`srs/srs.md`](srs/srs.md), [`nfr_quality_measures.md`](nfr_quality_measures.md) |

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
| TC-MNT-11 | US-13 | Return reaches the 10,000 km threshold while alert creation is forced to fail (fault injection, NFR-REL-02) | Whole return rolled back: no alert, reservation stays `ACTIVE`, vehicle stays `IN_USE`, odometer unchanged | I |

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
| TC-RES-11 | US-20 | Two concurrent `POST /reservations` for the same vehicle and period, repeated 20 times (NFR-REL-01, ADR-004) | Each run: exactly one `201` and one `409 RESERVATION_CONFLICT`; afterwards an SQL check finds 0 overlapping `CONFIRMED`/`ACTIVE` reservations | I |

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

Rule: consumption more than 25% above the vehicle's average, or litres above tank capacity, is flagged. The average (baseline) is the all-time average of the vehicle's completed full-tank intervals, excluding intervals flagged `CONSUMPTION_SPIKE`; it is used only after **at least 3** completed intervals. Partial fills (`fullTank = false`) between two full tanks are added to the next full-tank interval. `OUTSIDE_RESERVATION` does not depend on the average and is checked from the first receipt (`srs.md` REQ-FUE-02, F5).

| ID | User story | Scenario | Expected result | Level |
|----|-----------|----------|-----------------|-------|
| TC-FUEL-01 | US-29 | Valid receipt for an existing vehicle | `201`; unit price calculated | U, I |
| TC-FUEL-02 | US-29 | Litres or total price of 0 or below | `400 VALIDATION_ERROR` | I |
| TC-FUEL-03 | US-29 | Litres above the vehicle's tank capacity | `422 FUEL_EXCEEDS_TANK` | U, I |
| TC-FUEL-04 | US-29 | Receipt for a non-existent vehicle | `404 NOT_FOUND` | I |
| TC-FUEL-05 | US-30 | Two full-tank receipts 500 km apart, 40 L at the second | Consumption 8.0 L/100 km | U |
| TC-FUEL-06 | US-31 | Baseline 8.0 L/100 km from 3 completed intervals, new value 10.1 L/100 km (> 25%) | Receipt saved, anomaly `CONSUMPTION_SPIKE` | U |
| TC-FUEL-07 | US-31 | Baseline 8.0 L/100 km from 3 completed intervals, new value exactly 10.0 L/100 km (25%) | Not flagged | U |
| TC-FUEL-08 | US-31 | Receipt dated outside any reservation of the vehicle | Anomaly `OUTSIDE_RESERVATION` | U |
| TC-FUEL-09 | US-31 | Staff member requests the anomaly list | `403 FORBIDDEN` | I |
| TC-FUEL-10 | US-31 | Only 2 completed intervals (8.0 and 8.0 L/100 km); third interval 12.0 L/100 km | Receipt saved, **no** `CONSUMPTION_SPIKE` (fewer than 3 intervals) | U |
| TC-FUEL-11 | US-31 | 3 completed intervals of 8.0 L/100 km; fourth interval 10.1 L/100 km | `CONSUMPTION_SPIKE` (first interval that can be flagged) | U |
| TC-FUEL-12 | US-31 | Intervals 8.0, 8.0, 8.0; then 12.0 (flagged); then 10.1 | 12.0 flagged; baseline stays 8.0, so 10.1 is **also** flagged (if the flagged interval were counted, the baseline would be 9.0 and 10.1 would pass) | U |
| TC-FUEL-13 | US-31 | Intervals 7.0, 8.0, 9.0, 8.0, none flagged | Baseline (`baselineLPer100Km`) = 8.0, the all-time average | U, I |
| TC-FUEL-14 | US-30 | Full tank at 10,000 km; partial fill 15 L at 10,200 km; full tank 25 L at 10,500 km | One interval: (15 + 25) / 500 × 100 = 8.0 L/100 km | U |
| TC-FUEL-15 | US-31 | The vehicle's very first receipt is dated outside any reservation | Anomaly `OUTSIDE_RESERVATION` (no baseline needed) | U, I |

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
| TC-POOL-07 | US-24 | Two users join concurrently for the last free seat (NFR-REL-01, ADR-004) | One `201` and one `422 SEAT_CAPACITY_EXCEEDED`; passenger count never exceeds free seats | I |

### 6.8 Authentication and Authorisation

| ID | User story | Scenario | Expected result | Level |
|----|-----------|----------|-----------------|-------|
| TC-AUTH-01 | US-01 | Correct email and password | `200`; JWT and role returned | I |
| TC-AUTH-02 | US-01 | Wrong password | `401 INVALID_CREDENTIALS` | I |
| TC-AUTH-03 | US-01 | Any endpoint except login without a token | `401 UNAUTHORIZED` | I |
| TC-AUTH-04 | US-02 | Create a user with an existing email | `409 DUPLICATE_EMAIL` | I |

### 6.9 Driver Licences

Rule: a new licence starts with `verified = false`; only a fleet manager verifies it (US-04). `409 DUPLICATE_LICENSE` applies when the same licence number is submitted again or the driver already has a **non-expired** licence of the same class; a renewal after expiry is allowed and the expired record is kept (`srs.md` REQ-ID-03, #266). Licence data is personal data under KVKK: only the profile owner and `FLEET_MANAGER` may read or add it (`openapi.yaml`, #278).

| ID | User story | Scenario | Expected result | Level |
|----|-----------|----------|-----------------|-------|
| TC-LIC-01 | US-03 | Staff member adds a class B licence with number, issue date and a future expiry date to their own profile | `201`; licence returned with `verified = false`; it appears in `GET /drivers/{driverId}/licenses` | I |
| TC-LIC-02 | US-03 | A licence number that is already registered is added again | `409 DUPLICATE_LICENSE` | I |
| TC-LIC-03 | US-03 | Driver who already has a **non-expired** class B licence adds a second class B licence with a different number | `409 DUPLICATE_LICENSE` | I |
| TC-LIC-04 | US-03 | Expiry date is yesterday | `400 VALIDATION_ERROR` with a field error on `expiresAt` | U, I |
| TC-LIC-05 | US-03 | Expiry date is today (boundary: not in the past) | `201` | U |
| TC-LIC-06 | US-03 | Expiry date before the issue date | `400 VALIDATION_ERROR` | U, I |
| TC-LIC-07 | US-03 | Unknown licence class (`A2`) or licence number shorter than 3 or longer than 20 characters | `400 VALIDATION_ERROR` | I |
| TC-LIC-08 | US-03 | Licence added for a driver ID that does not exist | `404 NOT_FOUND` | I |
| TC-LIC-09 | US-03 | Staff member adds a licence to another user's profile | `403 FORBIDDEN` | I |
| TC-LIC-10 | US-03 | Staff member reads another user's licences (`GET /drivers/{driverId}/licenses`); a fleet manager reads the same list | Staff: `403 FORBIDDEN`; fleet manager: `200` | I |
| TC-LIC-11 | US-03 | Staff member opens another user's driver profile (`GET /drivers/{driverId}`) or checks another driver's eligibility | `403 FORBIDDEN` | I |
| TC-LIC-12 | US-03 | Driver's class B licence expired yesterday; a renewed class B licence with a new number and a future expiry date is added | `201`; new licence `verified = false`; the expired licence is still in `GET /drivers/{driverId}/licenses` | I |

### 6.10 Fleet Inventory

Rule: a new vehicle starts as `AVAILABLE`; the plate follows the Turkish format in `openapi.yaml` (`06 FS 104`); a maintenance plan is created for every active rule from the vehicle's current mileage.

| ID | User story | Scenario | Expected result | Level |
|----|-----------|----------|-----------------|-------|
| TC-VEH-01 | US-07 | Fleet manager adds a vehicle with valid data (example body in `openapi.yaml`) | `201`; status `AVAILABLE`; `maintenance.overallStatus` = `OK` | I |
| TC-VEH-02 | US-07 | Vehicle added with a plate that already exists | `409 DUPLICATE_PLATE` | I |
| TC-VEH-03 | US-07 | `odometerKm = -1` | `400 VALIDATION_ERROR` | U, I |
| TC-VEH-04 | US-07 | `seatCount = 0` | `400 VALIDATION_ERROR` | U, I |
| TC-VEH-05 | US-07 | Boundary values `odometerKm = 0` and `seatCount = 1` | `201` | U |
| TC-VEH-06 | US-07 | `tankCapacityLiters = 0`, or plate in a wrong format (`6 FS 104`, `06FS104`, `06 fs 104`) | `400 VALIDATION_ERROR` | U, I |
| TC-VEH-07 | US-07 | Staff member or maintenance officer tries to add a vehicle | `403 FORBIDDEN` | I |
| TC-VEH-08 | US-07 | Vehicle added with odometer 21,000 km | One maintenance plan per active rule, starting at 21,000 km and today's date; oil change rule `OK` | I |
| TC-VEH-09 | US-08 | Seed vehicles in `AVAILABLE`, `IN_USE` and `IN_MAINTENANCE`; list filtered by `status=AVAILABLE` | Only `AVAILABLE` vehicles returned; `page.totalElements` equals their number | I |
| TC-VEH-10 | US-08 | List without filters | Every vehicle returned with `status` and `maintenance` summary (`overallStatus`, `remainingKm`, `remainingDays`) | I |
| TC-VEH-11 | US-08 | Filters `type=MINIBUS` and `minSeats=9` | Only vehicles that match both filters | I |
| TC-VEH-12 | US-08 | Unknown status value (`status=BROKEN`) | `400 VALIDATION_ERROR` | I |
| TC-VEH-13 | US-08 | Details of a vehicle ID that does not exist | `404 NOT_FOUND` | I |
| TC-VEH-14 | US-08 | Vehicle ID that is not a valid UUID | `400 VALIDATION_ERROR` (not FastAPI's default `422`; ADR-003) | I |
| TC-VEH-15 | US-08 | List and details requested as `STAFF`, `FLEET_MANAGER` and `MAINTENANCE_OFFICER` | `200` for all three roles | I |

### 6.11 Maintenance Alert List

| ID | User story | Scenario | Expected result | Level |
|----|-----------|----------|-----------------|-------|
| TC-ALR-01 | US-14 | Two `OPEN` and one `RESOLVED` alert; list filtered by `status=OPEN` | Only the two `OPEN` alerts, newest `createdAt` first | I |
| TC-ALR-02 | US-14 | Alerts for three vehicles; list filtered by `vehicleId` | Only that vehicle's alerts | I |
| TC-ALR-03 | US-14 | List without filters | All alerts, `OPEN` and `RESOLVED`, sorted newest first; resolved alerts have `resolvedAt` | I |
| TC-ALR-04 | US-14 | Filter `level=DUE` combined with `status=OPEN` | Only open alerts of level `DUE` | I |
| TC-ALR-05 | US-14 | Filter by a vehicle that has no alerts | `200` with an empty `content` list | I |
| TC-ALR-06 | US-14 | Unknown status value (`status=CLOSED`) | `400 VALIDATION_ERROR` | I |
| TC-ALR-07 | US-13, US-43 | A return creates a `DUE` alert while a maintenance officer is signed in (notification, ADR-006) | `GET /maintenance/alerts?status=OPEN&size=1` shows `page.totalElements` increased by 1; the header badge and the alert list show it within one polling interval (60 s) | I, E |

### 6.12 Trip Destinations

| ID | User story | Scenario | Expected result | Level |
|----|-----------|----------|-----------------|-------|
| TC-LOC-01 | US-18 | Destinations from the demo seed data; list requested | Every seeded destination returned with `name`, `city` and `distanceKmFromBase` equal to the value in the seed data (US-47); no destination missing or duplicated | I |
| TC-LOC-02 | US-18 | Any destination in the list | `distanceKmFromBase` is a positive integer | I |
| TC-LOC-03 | US-18 | Staff member opens the trip request screen | Destination list filled from `GET /locations`; choosing one uses its distance for the request | E (part of TC-E2E-01) |

### 6.13 Reports: Carbon and Utilisation

Rules (`srs.md` REQ-REP-02 and REQ-REP-03, F3 and F4):
- **Carbon:** kg CO₂ = litres × factor; factors in kg CO₂/L: `GASOLINE` 2.31, `DIESEL` 2.68, `HYBRID` 2.31, `ELECTRIC` 0.0. Ride-sharing saving = passengers (driver excluded) × (actual trip km / 100) × the vehicle's average consumption (L/100 km) × factor; a vehicle without a full-tank average yet uses 8.0 L/100 km. Actual trip km = return odometer − pickup odometer (`tripKm`), not `estimatedKm`, so the value stays consistent with `FleetSummary.savedKm`.
- **Utilisation:** utilisation % = reserved hours / available hours × 100. Working hours are Monday–Friday 08:00–17:00 (9 h/day); weekends are excluded, public holidays are not. Only the part of a reservation inside working hours counts. `IN_MAINTENANCE` and `OUT_OF_SERVICE` time is removed from available hours.
- **Time zone:** times are stored in UTC; report periods and working hours are evaluated in Europe/Istanbul (UTC+3, no daylight saving) (`openapi.yaml`, #274).

| ID | User story | Scenario | Expected result | Level |
|----|-----------|----------|-----------------|-------|
| TC-REP-01 | US-35 | Diesel vehicle, 100 L of fuel in the period | `kgCo2` = 268.0 | U |
| TC-REP-02 | US-35 | Gasoline vehicle 50 L and hybrid vehicle 50 L | 115.5 kg each | U |
| TC-REP-03 | US-35 | Electric vehicle in the fleet | `kgCo2` = 0; `emissionFactors` contains all four fuel types | U, I |
| TC-REP-04 | US-35 | Diesel vehicle with average 7.5 L/100 km; completed trip with pickup 10,000 km and return 10,200 km (estimated 180 km), 2 passengers | `rideSharingSavedKgCo2` = 2 × 2 × 7.5 × 2.68 = 80.4 (uses the actual 200 km, not 180) | U |
| TC-REP-05 | US-35 | Gasoline vehicle with no full-tank average; completed trip of 100 actual km with 1 passenger | Default 8.0 L/100 km used: 1 × 1 × 8.0 × 2.31 = 18.48 | U |
| TC-REP-06 | US-35 | Trip with the driver only | Saving 0 | U |
| TC-REP-07 | US-35 | Several vehicles in the period | `totalKgCo2` equals the sum of the items | I |
| TC-REP-08 | US-36 | One full week (Monday–Sunday), no maintenance | `availableHours` = 45 (5 × 9) | U |
| TC-REP-09 | US-36 | Same week, 22.5 reserved working hours | `utilizationPercent` = 50 | U, I |
| TC-REP-10 | US-36 | Weekday reservation 16:00–20:00 | 1 reserved hour (16:00–17:00) | U |
| TC-REP-11 | US-36 | Reservation on Saturday 10:00–14:00 | 0 reserved hours; Saturday adds no available hours | U |
| TC-REP-12 | US-36 | Vehicle `IN_MAINTENANCE` all of Wednesday in a full week | `availableHours` = 36 | U |
| TC-REP-13 | US-36 | Reservation stored as 05:00–07:00 UTC (08:00–10:00 Istanbul) | 2 reserved hours (evaluated in Istanbul time, not UTC) | U |
| TC-REP-14 | US-36 | Reservations covering the whole period, including nights and the weekend | `utilizationPercent` = 100, never above | U |
| TC-REP-15 | US-36 | Period with `to` before `from` | `400 VALIDATION_ERROR` | I |
| TC-REP-16 | US-34 – US-36 | Staff member requests any report, as JSON or CSV | `403 FORBIDDEN` | I |
| TC-REP-17 | US-37 | Fleet manager requests `GET /reports/cost`, `/reports/carbon` and `/reports/utilization` with `Accept: text/csv` (ADR-006) | `200`, `text/csv`, UTF-8; one header row and one row per vehicle with the same values as the JSON `items`; `Content-Disposition: attachment; filename="fleetsync-<report>-<from>_<to>.csv"` | I |

### 6.14 Jury Demo Journey (E2E)

| ID | User stories | Scenario (`system_vision.md` §11) | Expected result | Level |
|----|-------------|-----------------------------------|-----------------|-------|
| TC-E2E-01 | US-40, US-19, US-12, US-20 | Staff member requests a vehicle; the vehicle near service is shown as blocked with its reason; a suitable vehicle is reserved | Blocked vehicle and reason visible; reservation `CONFIRMED` | E |
| TC-E2E-02 | US-41, US-24 | A colleague joins the ride | Passenger added; free seats decrease | E |
| TC-E2E-03 | US-42, US-26, US-27, US-13 | Pickup with checklist; return with mileage crossing 10,000 km | "10,000 km service is due" shown; vehicle `IN_MAINTENANCE` | E |
| TC-E2E-04 | US-43, US-15 | Maintenance officer sees the alert and records the service | Alert `RESOLVED`; vehicle `AVAILABLE` | E |
| TC-E2E-05 | US-45, US-34–36 | Fleet manager opens reports for the period | Cost, carbon and utilisation shown | E |

### 6.15 Non-Functional Test Cases

Test cases named in [`nfr_quality_measures.md`](nfr_quality_measures.md) §4. The other NFRs are verified by extending the functional test cases above (for example NFR-SEC-01 extends TC-AUTH-03 to every protected operation) or by the reports listed in the NFR document (Locust, Lighthouse, coverage, SonarQube).

| ID | NFR | Scenario | Expected result | Level |
|----|-----|----------|-----------------|-------|
| TC-NFR-PERF-02 | PERF-02 | Paginated lists (`GET /users`, `/vehicles`, `/reservations`, `/maintenance/alerts`) without parameters and with `size=101`; period-bounded lists (`GET /vehicles/{vehicleId}/fuel-receipts`, `/fuel/anomalies`, `/expenses`) with seed data spread over more than a year | Paginated: at most 20 items by default, `size=101` → `400 VALIDATION_ERROR`. Period-bounded: without `from`/`to` only the last 92 days; 366-day period → `200`; 367 days or `to` before `from` → `400 VALIDATION_ERROR` (#291) | I |
| TC-NFR-SEC-03 | SEC-03 | Create a user, then log in with an unknown email and with a wrong password; inspect the stored user | Password stored only as an Argon2id hash; password shorter than 8 characters → `400 VALIDATION_ERROR`; no response contains a password or hash field; both failed logins return the same `401 INVALID_CREDENTIALS` body | U, I |
| TC-NFR-SEC-04 | SEC-04 | Malformed input and `' OR 1=1 --` in text fields and query parameters of login, reservation and fuel receipt endpoints | `400 VALIDATION_ERROR` with field-level `errors`, or the value is stored as plain text; the result set never changes; no error body contains a stack trace, SQL text, file path or library name | I |
| TC-NFR-SEC-05 | SEC-05 | Licence data requested by the owner, a fleet manager and another staff member; logs collected during the E2E run | Owner and fleet manager see licence details; another staff member gets `403 FORBIDDEN`; logs contain no password, JWT or `JWT_SECRET` | I |
| TC-NFR-ACC-01 | ACC-01 | `axe-core` scan from the Playwright suite on the login, trip request, ride join, checklist, maintenance alerts and reports screens | 0 serious or critical violations; text contrast ≥ 4.5:1 (prototype palette already checked in `ui_ux_flow_and_dashboard.md` §8) | E |

## 7. Traceability: Must Stories and Their Test Cases

| User story | Test cases |
|---|---|
| US-01, US-02 | TC-AUTH-01 – TC-AUTH-04 |
| US-03 | TC-LIC-01 – TC-LIC-12 |
| US-04, US-05 | TC-ELG-01 – TC-ELG-05 |
| US-07 | TC-VEH-01 – TC-VEH-08 |
| US-08 | TC-VEH-09 – TC-VEH-15 |
| US-11 | TC-MNT-01 – TC-MNT-04 |
| US-12 | TC-REC-01 – TC-REC-03 |
| US-13 | TC-MNT-05 – TC-MNT-07, TC-MNT-11, TC-ALR-07, TC-E2E-03 |
| US-14 | TC-ALR-01 – TC-ALR-06, TC-E2E-04 |
| US-15 | TC-MNT-08, TC-MNT-09, TC-E2E-04 |
| US-18 | TC-LOC-01 – TC-LOC-03, TC-E2E-01 |
| US-19 | TC-REC-04 – TC-REC-06, TC-E2E-01 |
| US-20, US-21 | TC-RES-01 – TC-RES-05, TC-RES-07 – TC-RES-11, TC-E2E-01 |
| US-23, US-24 | TC-POOL-01 – TC-POOL-07, TC-E2E-02 |
| US-26, US-27 | TC-HND-01 – TC-HND-06, TC-E2E-03 |
| US-29 | TC-FUEL-01 – TC-FUEL-04 |
| US-34 | TC-REP-16, TC-E2E-05 (cost calculation tests follow with US-32 expenses) |
| US-35 | TC-REP-01 – TC-REP-07, TC-REP-16, TC-E2E-05 |
| US-36 | TC-REP-08 – TC-REP-16, TC-E2E-05 |
| US-45 | TC-E2E-05 |
| US-38 – US-43 | TC-E2E-01 – TC-E2E-05; US-43 also TC-ALR-07 |
| US-46 – US-51 | Verified by the CI pipeline itself (build, coverage report, E2E run) |

Since v0.4 every Must story has at least one test case (US-03, US-07, US-08, US-14 and US-18 were added in Sprint 2). Non-functional requirements are defined in [`nfr_quality_measures.md`](nfr_quality_measures.md) §4; the test cases they name are in §6.15 (TC-NFR-…) and in §6.1, §6.3 and §6.7 (TC-MNT-11, TC-RES-11, TC-POOL-07).

## 8. Acceptance Criteria Review (Sprint 1)

QA reviewed all acceptance criteria in `product_backlog.md` for testability and compared them with `system_vision.md` and `openapi.yaml`.

| # | Finding | Affected | Status |
|---|---|---|---|
| F1 | Demo step 5 says the maintenance officer is notified, but `openapi.yaml` had no notification endpoint. **Decision (ADR-006, #245):** a notification is an `OPEN` maintenance alert; the web app polls `GET /maintenance/alerts?status=OPEN&size=1` every 60 s and shows `page.totalElements` as a badge. | US-13, US-43 | Closed – ADR-006; TC-ALR-07 |
| F2 | CSV export is listed in `system_vision.md` §7.1 but had no endpoint in `openapi.yaml`. **Decision (ADR-006, #245):** CSV via `Accept: text/csv` on the cost, carbon and utilisation reports; no new paths. | US-37 | Closed – ADR-006; TC-REP-17 |
| F3 | The CO₂ factor per litre is not defined, so the carbon report cannot be checked against an expected value. **In SRS:** factors in `srs.md` REQ-REP-02 (gasoline and hybrid 2.31, diesel 2.68, electric 0.0 kg CO₂/L); `HYBRID` and `ELECTRIC` in `openapi.yaml` (#274). **PO decision 2026-11-21, not yet in SRS:** ride-sharing saving = passengers × (actual trip km / 100) × average L/100 km × factor, default 8.0 L/100 km. | US-35 | Decided – SRS update pending; TC-REP-01 – TC-REP-07 |
| F4 | "Available working hours" for utilisation is not defined. **In SRS:** Monday–Friday 08:00–17:00, maintenance and out-of-service time excluded (`srs.md` REQ-REP-03); Europe/Istanbul time zone (`openapi.yaml`, #274). **PO decision 2026-11-21, not yet in SRS:** only the overlap with working hours counts; weekends excluded, no public-holiday calendar. Note: US-36 criterion 1 ("20 of 40 working hours") cannot occur with 9-hour days; TC-REP-09 uses 22.5 of 45. | US-36 | Decided – SRS update pending; TC-REP-08 – TC-REP-15 |
| F5 | The number of earlier full-tank intervals needed before a fuel average is used is not defined. **In SRS:** at least 3 completed intervals (`srs.md` REQ-FUE-02); baseline excludes flagged intervals (`openapi.yaml` `baselineLPer100Km`, #278). **PO decision 2026-11-21, not yet in SRS:** flagged intervals are excluded from the baseline; partial fills join the next full-tank interval; `OUTSIDE_RESERVATION` is checked from the first receipt. | US-30, US-31 | Decided – SRS update pending; TC-FUEL-10 – TC-FUEL-15 |
| F6 | `POST /reservations` returns several error codes under the same HTTP status: 409 for vehicle problems (`RESERVATION_CONFLICT`, `VEHICLE_MAINTENANCE_DUE`, `VEHICLE_UNAVAILABLE`) and 422 for driver or request problems (`LICENSE_EXPIRED`, `LICENSE_CLASS_MISMATCH`, `SEAT_CAPACITY_EXCEEDED`). Tests check the `code` field, not only the HTTP status. | US-20 | Applied in this plan |
| F8 | The revised `openapi.yaml` (2026-11-02) returns `409 VEHICLE_MAINTENANCE_DUE` when a blocked vehicle is reserved; test plan v0.2 and `product_backlog.md` US-20 criterion 4 still said 422. Reported by the Backend Engineer in `carpool_reservation_api.md`.    Test plan fixed in v0.3 (#64); backlog fixed by the Product Owner (#66). | US-20 | Fixed | 
| F9 | The duplicate-licence rule differed between `product_backlog.md` (same number), `openapi.yaml` (same class) and `srs.md` (number/class). **Resolved (`srs.md` REQ-ID-03, #266):** 409 for the same number or a non-expired licence of the same class; renewal after expiry is allowed. | US-03 | Closed – TC-LIC-02, TC-LIC-03, TC-LIC-12 |
| F10 | The licence endpoints defined no `403` and no ownership rule, which conflicted with the KVKK constraint in `system_vision.md` §10 and NFR-SEC-05. **Resolved (#278):** profile, licence list, licence creation and eligibility are allowed only for the owner or `FLEET_MANAGER`, with `403 FORBIDDEN` otherwise. | US-03, US-04, US-05 | Closed – TC-LIC-09 – TC-LIC-11 |
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

- **Sprint 2:** Test cases for the remaining Must stories (done in v0.4); non-functional quality measures (`nfr_quality_measures.md` §4); F1, F2, F9 and F10 closed in v0.5; NFR test cases added in v0.6; F3–F5 decided, to be marked closed when the SRS contains the remaining PO decisions.
- **Sprint 3:** Coverage report from the CI pipeline; unit and integration tests implemented.
- **Final:** Integration and E2E test report; SonarQube summary.
