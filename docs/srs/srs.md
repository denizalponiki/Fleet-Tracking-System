# FleetSync · Software Requirements Specification (SRS)

| | |
|---|---|
| **Course** | SENG 321 Software Engineering · Sprint 2, Deliverable 1 |
| **Accountable (A) / Responsible (R)** | Ahmet Can Vurmaz (Product Owner & Requirements Engineer) |
| **Contributors** | Mehmet Umut Oğuzcan (`handover`), Deniz Alp Oniki (`reporting`), Ahmet Tarık Orhan (`reservation`, `carpool` review) |
| **Version** | 1.0 · Sprint 2 |
| **Related Documents** | [`product_backlog.md`](../product_backlog.md), [`openapi.yaml`](../openapi.yaml), [`test_plans_and_coverage.md`](../test_plans_and_coverage.md), [`traceability_matrix.md`](traceability_matrix.md) |

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) defines the functional requirements, business rules, user roles, and external interfaces for **FleetSync**, a smart institutional fleet management, predictive maintenance, and carpooling platform. It serves as the authoritative baseline for Sprint 3 implementation, API contract validation (`openapi.yaml`), and QA verification.

### 1.2 Scope
FleetSync manages institutional vehicles across their operational lifecycle: user authentication and driver eligibility verification (`identity`), fleet inventory (`vehicle`), mileage- and date-based predictive maintenance (`maintenance`), conflict-free vehicle recommendation and reservation (`reservation`), ride sharing (`carpool`), digital pickup/return checklists and damage reporting (`handover`), fuel receipt and anomaly tracking (`fuel`), and cost/carbon/utilisation analytics (`reporting`).

### 1.3 Definitions and Acronyms
- **JWT:** JSON Web Token (Bearer authentication).
- **RBAC:** Role-Based Access Control (`STAFF`, `FLEET_MANAGER`, `MAINTENANCE_OFFICER`).
- **RFC 9457:** Problem Details for HTTP APIs (`application/problem+json`).
- **Odometer Integrity:** Monotonically non-decreasing mileage rule across handovers, maintenance, and fuel logs.

---

## 2. Overall Description

### 2.1 User Classes and Roles
| Role | Description & Key Capabilities |
|---|---|
| **`STAFF`** | Institutional employee/driver. Requests vehicles, joins shared rides, completes pickup/return checklists, reports damages, records fuel receipts and trip expenses, manages own profile and driving licences. |
| **`FLEET_MANAGER`** | Manages user accounts and roles, verifies physical driving licences, manages vehicle inventory and maintenance rules, views all reservations, fuel anomalies, and fleet reports (cost, carbon, utilisation). |
| **`MAINTENANCE_OFFICER`** | Monitors open maintenance alerts and calendar, records completed services to reset intervals and release `IN_MAINTENANCE` vehicles back to `AVAILABLE`. |

### 2.2 Operating Environment & Constraints
- **Architecture:** Modular monolith backend (Python / FastAPI), React (Vite + Tailwind CSS) frontend, PostgreSQL database, containerized via Docker Compose (`docker compose up`).
- **API-First Contract:** All endpoints, payloads, status enums, and error codes must strictly match `docs/openapi.yaml`.
- **Privacy (KVKK):** Demo and seed datasets must contain only synthetic/invented personal data.

---

## 3. Functional Requirements

### 3.1 Identity, Access & Driver Eligibility (`identity` Module)
*Owner: Ahmet Can Vurmaz · Stories: US-01 to US-06*

#### REQ-ID-01: User Authentication & Session Management (US-01)
- **Trigger:** User submits email and password via `POST /auth/login`.
- **Behavior:**
  - The system shall validate credentials against stored salted password hashes.
  - On success (`200 OK`), the system shall return a signed JWT (`accessToken`), `tokenType: "Bearer"`, `expiresIn` (seconds, default `3600`), and the `User` object (`id`, `email`, `fullName`, `role`, `department`).
  - On invalid email or password, the system shall return `401 Unauthorized` with error code `INVALID_CREDENTIALS`.
  - Every API endpoint except `POST /auth/login` shall require a valid `Authorization: Bearer <JWT>` header. Missing, malformed, or expired tokens shall be rejected with `401 UNAUTHORIZED`.
  - Authenticated users shall retrieve their own session profile via `GET /me`.

#### REQ-ID-02: User Account & Role Management (US-02)
- **Access Control:** Restricted strictly to `FLEET_MANAGER`. Requests from `STAFF` or `MAINTENANCE_OFFICER` shall return `403 FORBIDDEN`.
- **Behavior:**
  - `GET /users` shall return a paginated list of users (`page`, `size`), optionally filtered by `role`.
  - `POST /users` shall create a new user account with `email`, `fullName` (2–100 chars), `role`, optional `department`, and `password` (min 8 chars), returning `201 Created`.
  - Duplicate email addresses shall be rejected with `409 DUPLICATE_EMAIL`.

#### REQ-ID-03: Driving Licence Registration (US-03)
- **Behavior:**
  - Drivers shall register licences via `POST /drivers/{driverId}/licenses` with `licenseClass` (`B`, `BE`, `C1`, `C`, `D1`, `D`), `licenseNumber` (3–20 chars), `issuedAt`, and `expiresAt`.
  - Every newly registered licence shall default to `verified = false`.
  - If `expiresAt` is in the past (or before `issuedAt`), the system shall reject with `400 VALIDATION_ERROR`.
  - Registering a duplicate licence number/class for the same driver shall return `409 DUPLICATE_LICENSE`.
  - **Licence Renewal Rule:** `409 DUPLICATE_LICENSE` applies only when the driver already has a non-expired licence of the same `licenseClass` or when the same `licenseNumber` is re-submitted. If an existing licence of that class is expired (`expiresAt < current date`), registering a renewed licence of the same class via `POST /drivers/{driverId}/licenses` is permitted (starting with `verified = false` until verified by a `FLEET_MANAGER`); the expired record is retained for audit history.
  - `GET /drivers/{driverId}` and `GET /drivers/{driverId}/licenses` shall return the driver profile (including computed `canDrive` boolean) and licence list.

#### REQ-ID-04: Driving Licence Verification (US-04)
- **Access Control:** Restricted to `FLEET_MANAGER` (`403 FORBIDDEN` otherwise).
- **Behavior:**
  - `POST /drivers/{driverId}/licenses/{licenseId}/verify` shall set `verified = true` after physical document inspection.
  - Only licences with `verified = true` shall be considered valid during eligibility checks.

#### REQ-ID-05: Driver Eligibility Evaluation (US-05)
- **Trigger:** `GET /drivers/{driverId}/eligibility?vehicleId={uuid}&endAt={date-time}` (also invoked internally during vehicle recommendation and reservation creation).
- **Behavior:**
  - The system shall evaluate whether the driver holds at least one **verified** licence matching the vehicle's `requiredLicenseClass` that remains valid on and after `endAt`.
  - If all conditions pass: `eligible = true`, `reasons = []`.
  - If the licence expires before `endAt`: `eligible = false`, reason code `LICENSE_EXPIRED`.
  - If the licence class does not cover the vehicle's required class: `eligible = false`, reason code `LICENSE_CLASS_MISMATCH`.
  - If no verified licence exists: `eligible = false` with explanatory reason.

#### REQ-ID-06: Driver Profile Update (US-06)
- **Access Control:** Allowed only for the profile owner (`driverId == currentUser.id`) or `FLEET_MANAGER`; otherwise `403 FORBIDDEN`.
- **Behavior:** `PUT /drivers/{driverId}` shall update `phone` (max 20 chars) and `employeeNo` (max 20 chars).

---

### 3.2 Fleet Inventory (`vehicle` Module)
*Owner: Ali Eren Kurt · Stories: US-07 to US-09*
- **REQ-VEH-01 (US-07):** `FLEET_MANAGER` adds vehicles (`POST /vehicles`) with Turkish plate validation, `seatCount >= 1`, `tankCapacityLiters > 0`, `odometerKm >= 0`. Initial status is `AVAILABLE`. Duplicate plates return `409 DUPLICATE_PLATE`.
- **REQ-VEH-02 (US-08):** All roles can list (`GET /vehicles`) with filters (`status`, `type`, `minSeats`) and view details (`GET /vehicles/{vehicleId}`).
- **REQ-VEH-03 (US-09):** `FLEET_MANAGER` updates metadata (`PATCH /vehicles/{vehicleId}`). Manual status changes (`POST /vehicles/{vehicleId}/status`) allow `AVAILABLE → IN_MAINTENANCE/OUT_OF_SERVICE` and `OUT_OF_SERVICE → IN_MAINTENANCE`. Manually setting `IN_MAINTENANCE → AVAILABLE` or changing `IN_USE` manually is rejected with `409 INVALID_STATUS_TRANSITION`.

### 3.3 Predictive Maintenance (`maintenance` Module)
*Owner: Ali Eren Kurt · Stories: US-10 to US-17*
- **REQ-MNT-01 (US-10, US-11):** Default rules: `OIL_CHANGE` (10,000 km / 12 mo, warn 1,000 km / 30 days), `TIRE_LIFE` (40,000 km / 48 mo, warn 2,000 km / 60 days), `INSPECTION` (24 mo, warn 30 days). Rule status evaluates to `OK`, `DUE_SOON`, or `DUE`.
- **REQ-MNT-02 (US-12):** A vehicle is blocked for a trip if `remainingKm < estimatedKm + 100` (safety buffer) or if any rule's due date falls before `endAt`, returning reason `MAINTENANCE_DUE`.
- **REQ-MNT-03 (US-13, US-14, US-15):** On vehicle return, if any rule reaches `DUE`, the system automatically creates an `OPEN` alert and transitions the vehicle to `IN_MAINTENANCE`. Only a `MAINTENANCE_OFFICER` recording a service (`POST /maintenance/records`) resolves alerts and releases the vehicle to `AVAILABLE` (if no other rule is `DUE`). Decreasing odometer returns `422 ODOMETER_DECREASED`.

### 3.4 Reservations & Vehicle Recommendation (`reservation` Module)
*Owner: Ahmet Tarık Orhan · Stories: US-18 to US-22*
- **REQ-RES-01 (US-18, US-19):** Predefined destinations (`GET /locations`) provide distances. `GET /vehicles/recommendations` evaluates vehicles in order: seat capacity → driver eligibility → calendar conflicts → maintenance rules → scoring, returning both `recommended` and `blocked` lists with explicit reason codes.
- **REQ-RES-02 (US-20, US-21, US-22):** `POST /reservations` re-validates all rules server-side (max 14-day duration). Overlaps return `409 RESERVATION_CONFLICT`; back-to-back periods (e.g., 10:00–12:00 and 12:00–14:00) are permitted. Only `CONFIRMED` reservations can be cancelled (`409 RESERVATION_NOT_CANCELLABLE` if `ACTIVE`).

### 3.5 Ride Sharing (`carpool` Module)
*Owner: Ahmet Tarık Orhan · Stories: US-23 to US-25*
- **REQ-CRP-01 (US-23):** `GET /rides/matches` matches `CONFIRMED` reservations with the same `destinationId`, `allowRideSharing = true`, sufficient `seatsAvailable`, and departure within `toleranceMinutes` (default `30` minutes).
- **REQ-CRP-02 (US-24, US-25):** Staff join via `POST /reservations/{id}/passengers` (`422 SEAT_CAPACITY_EXCEEDED` if full, `409 ALREADY_JOINED` if duplicate) and leave before trip start via `DELETE` (`409 INVALID_RESERVATION_STATE` if `ACTIVE`).

### 3.6 Vehicle Handover (`handover` Module)
*Contributor: Mehmet Umut Oğuzcan · Stories: US-26 to US-28*
- **REQ-HND-01 (US-26):** Pickup (`POST /reservations/{id}/pickup`) requires all mandatory checklist items (`422 CHECKLIST_INCOMPLETE`) and `odometerKm >= vehicle.odometerKm` (`422 ODOMETER_DECREASED`). Transitions reservation to `ACTIVE` and vehicle to `IN_USE`.
- **REQ-HND-02 (US-27):** Return (`POST /reservations/{id}/return`) computes `tripKm = returnOdometer - pickupOdometer`, flags `kmLimitExceeded = true` if `tripKm > estimatedKm * 1.30`, transitions reservation to `COMPLETED`, and triggers the maintenance rule engine in the same transaction.
- **REQ-HND-03 (US-28):** Damage reports (`POST /damage-reports`) record `MINOR`, `MODERATE`, or `SEVERE` damage. `SEVERE` damage transitions the vehicle to `OUT_OF_SERVICE`.

### 3.7 Fuel & Expenses (`fuel` Module)
*Owner: Abdullah Tecimen · Stories: US-29 to US-32*
- **REQ-FUE-01 (US-29, US-30):** `POST /fuel-receipts` validates positive values (`400 VALIDATION_ERROR`), `liters <= tankCapacityLiters` (`422 FUEL_EXCEEDS_TANK`), and non-decreasing odometer (`422 ODOMETER_DECREASED`). Consumption (L/100 km) is calculated between consecutive full-tank receipts.
- **REQ-FUE-02 (US-31, Business Rule F5):** Once a vehicle has at least **3 completed full-tank intervals** establishing its baseline average, any new full-tank interval exceeding the baseline by **> 25%** is saved and flagged `CONSUMPTION_SPIKE`. Receipts dated outside any reservation are flagged `OUTSIDE_RESERVATION`. `GET /fuel/anomalies` is restricted to `FLEET_MANAGER`.
- **REQ-FUE-03 (US-32):** Non-fuel expenses (`TOLL`, `PARKING`, `CAR_WASH`, `BRIDGE`, `OTHER`) are recorded via `POST /expenses` with `amount > 0`.

### 3.8 Reporting (`reporting` Module)
*Contributor: Deniz Alp Oniki · Stories: US-33 to US-37*
- **Access Control:** All `/reports/*` endpoints require `FLEET_MANAGER` (`403 FORBIDDEN` for other roles).
- **REQ-REP-01 (US-33, US-34):** `GET /reports/summary` and `GET /reports/cost` aggregate fleet status counts, open alerts, fuel, expense, and maintenance costs for `[from, to]`.
- **REQ-REP-02 (US-35, Business Rule F3):** `GET /reports/carbon` calculates `kg CO₂ = liters × emissionFactor` using documented factors: `GASOLINE: 2.31`, `DIESEL: 2.68`, `HYBRID: 2.31`, `ELECTRIC: 0.00` kg CO₂/L, and reports `rideSharingSavedKgCo2`.
- **REQ-REP-03 (US-36, Business Rule F4):** `GET /reports/utilization` computes `utilizationPercent = (reservedHours / availableHours) × 100`, where working hours are **weekdays (Mon–Fri) 08:00–17:00 (9 hours/day)**, excluding `IN_MAINTENANCE` and `OUT_OF_SERVICE` periods.
- **REQ-REP-04 (US-37):** Reports support CSV download via `Accept: text/csv`.

---

## 4. External Interface Requirements
- **API Interface:** RESTful JSON API over HTTP/HTTPS defined in `docs/openapi.yaml` (base path `/api/v1`). Errors conform to RFC 9457 (`application/problem+json`) with machine-readable `code` fields.
- **User Interface:** Responsive web application covering all three roles, specified in `docs/ui_ux_flow_and_dashboard.md` and Figma prototypes.

## 5. Non-Functional Requirements
Detailed measurable quality targets (response time, ≥ 50% backend unit test coverage, security, availability, single-command Docker deployment, and backup/recovery) are specified in `docs/nfr_quality_measures.md`.
