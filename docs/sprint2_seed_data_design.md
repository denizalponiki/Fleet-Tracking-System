# FleetSync — Sprint 2 Synthetic Demo Seed Data Design

| Field | Value |
|---|---|
| Phase / scope | **Sprint 2: requirements and test-data design only** |
| Author | Deniz Alp Oniki — DevOps & CI/CD Infrastructure Engineer |
| Review | Ali Eren Kurt — Lead Architect; domain owners verify their records |
| Date | 2026-11-21 |
| Tracking | [Issue #284](https://github.com/denizalponiki/Fleet-Tracking-System/issues/284), future [US-47 #104](https://github.com/denizalponiki/Fleet-Tracking-System/issues/104) |
| Status | Proposed design for review; **not implemented or loaded** |

## 1. Purpose and source of truth

The Sprint 2 deliverable is a **design specification** for a reproducible, entirely fictional jury-demo dataset. It describes records and relationships that the future Sprint 3 seed implementation (US-47) must create. This document contains **no SQL, scripts, actual account credentials, or personal data**.

Authoritative sources:
- [System vision and seven demo steps](system_vision.md#11-release-1-at-a-glance)
- [OpenAPI examples](openapi.yaml), especially vehicle recommendation, pickup, return and service examples
- [API usage and vehicle examples](api_usage.md)
- [SRS functional requirements](srs/srs.md)
- [ER diagram / table ownership](uml/er_diagram.md)
- [Sprint 2 plan](sprint-reports/sprint-2.md)

Values labelled **Contract example** are already present in OpenAPI or API usage. Values labelled **Proposed fixture** are candidates requiring owner approval; they should not silently become additional product requirements.

## 2. Seed record inventory and relationships

| Domain / ER entities | Minimum planned seed records | Purpose and source | Review owner |
|---|---|---|---|
| Identity: `app_user`, `driver_profile`, `driving_license` | At least one fictional `STAFF` driver, a second `STAFF` ride participant, one `FLEET_MANAGER`, and one `MAINTENANCE_OFFICER`. Driver has a verified, unexpired compatible licence through the entire trip. | Supports authorization, eligibility, carpool and service steps; SRS §3.1 | Product Owner |
| Fleet: `vehicle`, `vehicle_status_change` | Three canonical example vehicles `06 FS 101`, `06 FS 102`, `06 FS 103` | Matches [API usage](api_usage.md) and recommendation examples in OpenAPI | Architect |
| Maintenance: `maintenance_rule`, `maintenance_plan` | Oil-change rule and vehicle-specific last-service readings; optionally tyre and inspection rules with non-blocking dates | Produces one blocked vehicle and one vehicle becoming due on return; system vision §8 | Architect |
| Destination: `location` | A predefined **Konya** destination and a distance assumption matching the recommendation request | Demo destination from existing OpenAPI examples; reservation owner confirms location ID | Backend owner |
| Reservations: `reservation` and `ride_passenger` | A valid demo reservation on the eligible vehicle, plus a second staff member joining the ride | Steps 1–3; no overlapping confirmed/active reservation | Backend owner |
| Handover: `handover_record`, `handover_item` | Required pickup and return checklist items, with mileage and fuel level | Steps 4–5; checklist templates/required items from current contract | Scrum Master / handover owner |
| Maintenance outcome: `maintenance_alert`, `maintenance_record`, `maintenance_record_rule` | An `OPEN` due alert on return; service record resolves it | Steps 5–6; record created by the scenario, not necessarily preloaded | Architect |
| Reporting: `fuel_receipt`, `expense`, service costs | Fictional receipt, expense and maintenance cost records, tied to the demo vehicle/period | Step 7 cost, carbon and utilisation; SRS §3.8 | Reporting owner + QA |

**Timing rule:** Distinguish **initial seed state** (before the jury actions) from **records created during the demo** (reservation, ride membership, pickup/return, new alert, service). Preloading completed demo outcomes can invalidate the flow or make the vehicle unavailable. A fresh reset must reproduce the same initial conditions.

## 3. Canonical vehicles and decision logic

| Vehicle | Grounded OpenAPI example | Expected behavior in the demo |
|---|---|---|
| **06 FS 101** | Minibus, 9 seats, starting odometer **39,900 km**; oil change due in **100 km** | **Blocked by maintenance** for a 400 km planned trip plus the 100 km safety buffer |
| **06 FS 102** | Minibus, 9 seats, starting odometer **59,450 km**; oil change due at **60,000 km** (550 km remaining) | **Recommended** for 7 seats and 400 estimated km, because 550 km is greater than the required 500 km margin |
| **06 FS 103** | Sedan, 5 seats, starting odometer **12,300 km** | **Blocked by insufficient seats** for a 7-seat request |

These are examples in `docs/openapi.yaml` and `docs/api_usage.md`, not invented production records. The vehicle recommendation request uses `estimatedKm=400` and `seats=7`. The rule from `system_vision.md` §8 is: block when `remainingKm < estimatedKm + 100` (or a due date falls before trip end).

The OpenAPI return example has `06 FS 102` returned at **60,020 km**. Thus `tripKm = 60,020 - 59,450 = 570 km`. With an estimated 400 km, 570 is above the 30% permitted excess (520 km), so the **`kmLimitExceeded` flag is expected to be true**, consistent with the OpenAPI response. The same return reaches the 60,000 km service point, creates a due alert and puts the vehicle into `IN_MAINTENANCE`.

**Constraint to review:** Existing OpenAPI examples use historical timestamps (November 2026). The seed implementer must select a fixed, internally consistent, replayable demonstration time and avoid expired licences or past-due calendar conflicts when running the jury demo. Do not silently change the API's canonical sample IDs, plates, odometers or state transitions.

## 4. Seven-step demo data sequence

| Step | Initial data / action | Expected data result | Source |
|---|---|---|---|
| 1. Request | Fictional STAFF with compatible verified licence; destination Konya; 7 seats; estimated 400 km | Eligibility passes and candidate vehicles are evaluated | System vision §11, SRS §3.4 |
| 2. Recommend | `06 FS 101` has 100 km until service; `06 FS 102` has 550 km; `06 FS 103` has only 5 seats | 101 blocked for maintenance; 102 recommended; 103 blocked for capacity | OpenAPI recommendation examples |
| 3. Reserve and share | Reserve 102 for the designated period, with no overlap; second fictional staff user joins | `CONFIRMED` reservation, one ride passenger record | System vision §11, SRS §§3.4–3.5 |
| 4. Pickup | Required checklist completed; pickup odometer 59,450 km; OpenAPI example fuel level 90% | Pickup handover saved; reservation becomes `ACTIVE`; vehicle is `IN_USE` | OpenAPI pickup example |
| 5. Return / trigger | Return odometer 60,020 km; OpenAPI example fuel level 35% | Reservation `COMPLETED`; 570 km trip with excess-mileage flag; `DUE` / `OPEN` oil alert; vehicle `IN_MAINTENANCE` | OpenAPI return example and SRS |
| 6. Service | Maintenance officer records an oil service, linked to the open alert | Alert resolved and vehicle `AVAILABLE` only if no other maintenance rule is due | System vision §11, SRS §3.3 |
| 7. Report | Manager chooses a period covering the demo trip; fictional fuel, expense, and maintenance costs exist | Fleet summary, cost, CO₂ and utilisation are calculable for the period | SRS §3.8, ADR-006 |

## 5. Required consistency and safety constraints

1. **Referential integrity:** Every foreign key must resolve to a seeded or demo-created entity per `uml/er_diagram.md`; the same vehicle and reservation identifiers appear across handover, fuel and service.
2. **Role security:** Manager-only `/reports/*` endpoints stay inaccessible to STAFF (`403 FORBIDDEN`); only the maintenance officer performs the service action under the SRS rules.
3. **Licences:** Driver's required licence class, verification and expiry must be valid through the trip end; synthetic names/identifiers only.
4. **Status consistency:** Start with 102 `AVAILABLE` and no conflicting reservation. Transition through `IN_USE`, `IN_MAINTENANCE` and back to `AVAILABLE` as the demo proceeds.
5. **Deterministic reruns:** Document reset semantics for the *future* seed implementation. Running the demo must not leave overlapping reservations, duplicate open alerts or stale state in the next run.
6. **No embedded credentials:** Future demo users may be specified by role, but never add reusable passwords, JWTs, private keys or real licence details in a committed seed document.
7. **Reporting period:** Use the SRS-defined Europe/Istanbul business time and Monday–Friday 08:00–17:00 availability calendar. Choose a reporting period containing the created trip, and reconcile all cost components to source records.

## 6. Proposed fixture values requiring domain review

The current references do **not** finalize these details, so they are deliberately not presented as established facts:

- Fictional user labels and deterministic UUIDs for every user, licence, reservation, location and receipt.
- Actual `vehicle_type`, fuel type, licence-class, tank and service-date details beyond the displayed API examples.
- Exact default checklist template IDs/items and any mandatory item set.
- An approved date/time anchor for the demo and compatible licence validity intervals.
- Full fuel/expense/maintenance fixtures and whether the report starts with history or uses only newly generated demo records.
- Zero-available-hours handling and ride-sharing CO₂ savings estimation methodology for report calculations.

**Existing API examples** already include a fictional 48.5 L fuel receipt for the demo vehicle, a 4,850.00 service cost, and a 570 km trip. If the team uses those numbers, cross-check the cost/report response examples rather than altering calculated totals independently.

## 7. Acceptance checklist for Sprint 2 review

- [ ] PO validates actors, licence eligibility, and demo period.
- [ ] Architect checks vehicle/maintenance examples and entity references.
- [ ] Reservation/handover owners confirm sequence assumptions and required checklist records.
- [ ] QA verifies that the design produces the expected blocking, excess-mileage and post-return maintenance cases.
- [ ] Reporting owner confirms consistent reporting source data and access rules.
- [ ] Lead Architect approves this **design**, without claiming future US-47 implementation is complete.

**Out of scope:** seed scripts, migrations, Docker Compose updates, real accounts, database population, and running end-to-end tests. Those belong to implementation/testing phases after Sprint 2.
