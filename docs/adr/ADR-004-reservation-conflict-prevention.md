# ADR-004: Reservation conflicts are prevented by the database

- Status: Accepted
- Date: 2026-11-21
- Decider: Ali Eren Kurt (Lead Software Architect)
- Consulted: Ahmet Tarık Orhan (Backend & API, reservation owner), Abdullah Tecimen (QA)

## Context

Goal G2 in `docs/system_vision.md` is **zero** overlapping confirmed reservations for the
same vehicle. A check in application code alone ("is there an overlapping reservation?"
then "insert") has a race: two staff members who reserve the same vehicle at the same
moment both see no conflict and both insert. The same race exists for the last free seat
in a shared ride. Back-to-back trips (10:00–12:00 and 12:00–14:00) must be allowed
(`docs/carpool_reservation_api.md`, US-20).

## Decision

1. **Exclusion constraint.** The `reservation` table has

   ```sql
   EXCLUDE USING gist (
       vehicle_id WITH =,
       tstzrange(start_at, end_at, '[)') WITH &&
   ) WHERE (status IN ('CONFIRMED','ACTIVE'))
   ```

   (extension `btree_gist`). Periods are half-open `[start, end)`, so back-to-back trips
   do not overlap. Cancelled and completed reservations do not block the period.
2. **Service check first, constraint as the guarantee.** `reservation.service` still
   queries for an overlap before inserting, so the normal case returns a clear
   `409 RESERVATION_CONFLICT` with `suggestedVehicleIds`. If two requests race, the
   constraint rejects the second insert with SQLSTATE `23P01`, which the repository maps
   to the same `409 RESERVATION_CONFLICT`.
3. **Row lock on the vehicle.** Creating a reservation runs `SELECT ... FOR UPDATE` on the
   vehicle row, so a concurrent status change (for example to `IN_MAINTENANCE`) cannot
   slip between the checks and the insert.
4. **Seats.** Joining a ride locks the reservation row (`SELECT ... FOR UPDATE`) before
   counting passengers, so two people cannot take the last seat. The composite primary key
   `(reservation_id, user_id)` on `ride_passenger` prevents joining twice
   (`409 ALREADY_JOINED`).
5. Isolation level stays PostgreSQL's default `READ COMMITTED`.

## Alternatives considered

| Option | Why not |
|---|---|
| Application check only | Race condition; G2 cannot be guaranteed |
| `SERIALIZABLE` isolation for every request | Correct, but serialization failures must be retried in every endpoint; harder for the team to reason about |
| Table lock or advisory lock per vehicle for every reservation | Works, but the database already offers a declarative rule that also protects data written by scripts and seeds |
| Store time slots (one row per hour) with a unique index | Wastes rows, breaks for minute-level times, and makes "back-to-back" rules awkward |

## Consequences

- Positive: G2 holds even under concurrent requests and for data inserted outside the API.
- Positive: the rule is visible in the schema (`docs/uml/er_diagram.md` §4–§5).
- Negative: ties the design to PostgreSQL (`tstzrange`, `btree_gist`). SQLite cannot be
  used for integration tests; they run against PostgreSQL in Docker.
- Follow-up: an integration test sends two concurrent `POST /reservations` for the same
  vehicle and period and expects exactly one `201` and one `409` (Sprint 3, TC-RES).

## Related

- `docs/system_vision.md` §4 G2, §8 No double booking
- `docs/uml/sequence_diagrams.md` SD-3, SD-4
- `docs/uml/er_diagram.md` §4 `reservation`, `ride_passenger`
- Issue #242
