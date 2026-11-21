# FleetSync · Domain Event Contracts

> SENG 321 · Sprint 2. Owners: Mehmet Umut Oğuzcan (`handover`, publisher) and Ali Eren Kurt (Architect, `maintenance` consumer).
> Status: **draft for review**. Related: [ADR-002](adr/ADR-002-modular-monolith.md) · [C4 §3.1](c4/README.md) · [SD-6](uml/sequence_diagrams.md) · [`openapi.yaml`](openapi.yaml) `recordReturn`

Domain events let a lower module react to a higher one without importing it (ADR-002 rule 3). They are synchronous and in-process: the event bus in `app/shared/events.py` calls every handler immediately, inside the caller's database transaction (ADR-002 rule 4).

## 1. General rules

| Rule | Decision |
|---|---|
| Naming | Past tense, no `Event` suffix in code: `TripCompleted`, `SevereDamageReported`. Documents may say "the `TripCompleted` event". |
| Location | Each event is a frozen dataclass in the publisher's `events.py` and is re-exported from its `api.py`. Consumers import only from `api.py`. |
| Payload | IDs and values only, never ORM objects. All fields are required. |
| Time | `occurredAt` is UTC (`datetime` with `tzinfo`). |
| Transaction | Published after the publisher's own writes and before the commit. If a handler raises, the whole request rolls back and returns the handler's error. |
| Return value | A handler may return a list of results (for `TripCompleted`: the alerts it opened); the bus returns them to the publisher. |
| Idempotency | Each handler must be safe to run once per event; `eventId` lets it detect a repeat. |

## 2. `TripCompleted`

**Publisher:** `handover`, in `POST /reservations/{reservationId}/return` (US-27), once per successful return.
**Consumer:** `maintenance` · `MaintenanceRuleEngine.onTripCompleted()` (US-13).
**Purpose:** evaluate the vehicle's maintenance rules with the new odometer and date; open alerts; move the vehicle to `IN_MAINTENANCE` when any rule is `DUE`.

| Field | Type | Meaning | Used by |
|---|---|---|---|
| `eventId` | UUID | Unique per event | idempotency |
| `occurredAt` | datetime (UTC) | Time of the return | date-based rules (`intervalMonths`) |
| `reservationId` | UUID | Completed reservation | alert link, logs |
| `vehicleId` | UUID | Returned vehicle | rule evaluation |
| `odometerKm` | int | Odometer at return (already saved on the vehicle) | km-based rules (`intervalKm`) |
| `tripKm` | int | `odometerKm` − pickup odometer | logs, future reports |
| `severeDamageReported` | bool | A `SEVERE` damage was recorded in this return | vehicle status priority (§4) |

```python
# backend/app/modules/handover/events.py
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class TripCompleted:
    event_id: UUID
    occurred_at: datetime
    reservation_id: UUID
    vehicle_id: UUID
    odometer_km: int
    trip_km: int
    severe_damage_reported: bool
```

**Example (demo step 5):** pickup at 59,450 km, return at 60,020 km, oil change due at 60,000 km.

```json
{
  "eventId": "8f1c2b4e-1a7d-4c55-9b0e-2f3a4d5e6f70",
  "occurredAt": "2026-12-03T16:40:00Z",
  "reservationId": "c3a1e9d2-5b6f-4a7c-8d9e-0f1a2b3c4d5e",
  "vehicleId": "a7b8c9d0-1e2f-4a3b-9c4d-5e6f7a8b9c0d",
  "odometerKm": 60020,
  "tripKm": 570,
  "severeDamageReported": false
}
```

→ `maintenance` opens a `DUE` alert, sets the vehicle to `IN_MAINTENANCE` and returns the alert; `ReturnResult.maintenanceAlerts` carries it to the client.

## 3. `SevereDamageReported`

**Publisher:** `handover`, in `POST /damage-reports` (US-28) and in a return that contains a `SEVERE` damage.
**Consumer:** none in release 1. `handover` sets the vehicle to `OUT_OF_SERVICE` through `vehicle/api.py` directly (allowed dependency `handover → vehicle`).
**Decision needed (§5, Q2):** keep the event for a future notification consumer, or remove it from C4 §3.1 until it has a consumer.

| Field | Type |
|---|---|
| `eventId` | UUID |
| `occurredAt` | datetime (UTC) |
| `damageReportId` | UUID |
| `vehicleId` | UUID |
| `reservationId` | UUID or null (report outside a trip) |

## 4. Order inside the return transaction

1. Validate: reservation `ACTIVE`, return odometer ≥ pickup odometer (else 422 `ODOMETER_DECREASED`), required checklist items present.
2. Insert the `RETURN` handover record, its items and its damages.
3. Compute `tripKm` and `kmLimitExceeded` (`tripKm > estimatedKm × 1.3`).
4. `vehicle.updateOdometer(odometerKm)`.
5. `reservation.complete()` → `COMPLETED`.
6. Publish `TripCompleted` → `maintenance` evaluates, opens alerts, sets `IN_MAINTENANCE` or `AVAILABLE`.
7. If `severeDamageReported`: set `OUT_OF_SERVICE`. **Severe damage overrides the maintenance status** (state diagram: `IN_USE → OUT_OF_SERVICE : return with SEVERE damage`).
8. Commit; respond `201 ReturnResult`.

## 5. Open questions for the review with the Architect

| # | Question | Proposal |
|---|---|---|
| Q1 | C4 §3.1 says `maintenance` also consumes `VehicleOdometerUpdated`, but `vehicle` publishes no events. If step 4 published it, the rules would run twice in one return and could open duplicate alerts. | Remove `VehicleOdometerUpdated` for release 1; `TripCompleted` is the only trigger. A manual odometer correction (US-09) calls `maintenance/api.py` explicitly if needed. |
| Q2 | `SevereDamageReported` has no consumer. | Remove it from C4 §3.1 for release 1, or mark it "reserved for notifications (F1)". |
| Q3 | SD-6 shows `TripCompleted(vehicleId, odometerKm)` only. | Use the field list in §2; update SD-6 and the class diagram to match. |
| Q4 | Who runs `onTripCompleted` tests? | Unit tests in `maintenance` (9,999 / 10,000 / 10,050 km cases, T-13.3); an integration test of the full return in `handover` (T-27.3, #207). |

## 6. Traceability

| Item | Link |
|---|---|
| Stories | US-27 (#129), US-28 (#130), US-13 (#98) |
| Tasks | T-27.3 Publish TripCompletedEvent (#207) |
| Endpoint | `POST /reservations/{reservationId}/return` → `ReturnResult` |
| Diagrams | SD-6 in `uml/sequence_diagrams.md`; vehicle state machine in `uml/state_diagrams.md` |
