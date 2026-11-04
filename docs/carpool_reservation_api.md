# FleetSync · Reservation and Carpool API

| | |
|---|---|
| Course | SENG 321 Software Engineering · Sprint 1 |
| Owner | Ahmet Tarık Orhan, Implementation & Integration Engineer (Backend & API) |
| Version | 0.1 · Sprint 1 |
| Related documents | `openapi.yaml`, `api_usage.md`, `product_backlog.md` (Epics E4, E5), `system_vision.md` §8 |

## Endpoints

These operations belong to the `locations`, `reservations` and `carpool` tags. Every call needs `Authorization: Bearer <JWT>`.

| Endpoint | What it does | User story |
|---|---|---|
| `GET /locations` | Returns the predefined destinations a staff member can choose, each with its city and the one-way road distance from the main campus. | US-18 |
| `GET /vehicles/recommendations` | Takes a time window, the number of seats and the estimated distance, then returns the vehicles that pass every check (highest score first) and lists the rejected ones with a reason. | US-19 |
| `POST /reservations` | Holds a vehicle for a trip. The server runs the recommendation checks again and, when they pass, stores the reservation as `CONFIRMED`. | US-20 |
| `GET /reservations`, `GET /reservations/{id}` | Lists reservations and returns one of them. A staff member sees only their own reservations and the rides they joined; a fleet manager sees the whole calendar. | US-21 |
| `POST /reservations/{id}/cancel` | Cancels a reservation the caller no longer needs, sets it to `CANCELLED` and frees that period for someone else. | US-22 |
| `GET /rides/matches` | Finds existing trips to the same destination that leave within the tolerance window and still have free seats. | US-23 |
| `POST /reservations/{id}/passengers` | Adds the signed-in user to that ride as a passenger and reduces the free-seat count by one. | US-24 |
| `DELETE /reservations/{id}/passengers/{userId}` | Removes a passenger from a ride that has not started yet and gives the seat back. | US-25 |

## Business rules and errors

The rules below are the ones in `system_vision.md` §8 that this module implements. Error bodies are RFC 9457 `application/problem+json`; clients branch on `code`. The codes are the ones in `openapi.yaml`.

Shared responses on these operations:

- Missing or invalid token → `401 UNAUTHORIZED`
- Unknown vehicle, destination, reservation or user → `404 NOT_FOUND`
- The caller's role or ownership does not allow the operation → `403 FORBIDDEN`
- A field is missing or out of range → `400 VALIDATION_ERROR` (the body includes an `errors` array)

**No double booking.** A vehicle cannot hold two `CONFIRMED` or `ACTIVE` reservations whose periods overlap. An overlap is rejected with `409 RESERVATION_CONFLICT`. Back-to-back periods are not an overlap: 10:00–12:00 and 12:00–14:00 on the same vehicle are both accepted (US-20).

**Vehicle blocked for maintenance.** A vehicle is not offered for a trip when, for any maintenance rule, remaining kilometres are less than the estimated trip plus a 100 km safety buffer, or the rule's due date falls before the trip ends (`system_vision.md` §8, trip blocking). `GET /vehicles/recommendations` keeps that vehicle in `blocked` with `MAINTENANCE_DUE` or `MAINTENANCE_DUE_SOON`. Calling `POST /reservations` anyway is rejected with `409 VEHICLE_MAINTENANCE_DUE`. The body may include `suggestedVehicleIds`. A vehicle that is already `IN_MAINTENANCE` or `OUT_OF_SERVICE` is rejected with `409 VEHICLE_UNAVAILABLE`.

`product_backlog.md` US-20 acceptance criterion 4 and `test_plans_and_coverage.md` (TC-RES-04, note F6) still describe the maintenance case as `422 VEHICLE_MAINTENANCE_DUE`. This note follows the contract. The mismatch is filed for the lead architect in #52.

**Driver licence.** The driver needs a verified licence of a class that allows the vehicle, still valid when the trip ends. Otherwise `POST /reservations` returns `422 LICENSE_EXPIRED` or `422 LICENSE_CLASS_MISMATCH`. The same reasons can appear on a blocked recommendation (`LICENSE_EXPIRED`, `LICENSE_CLASS_MISMATCH`).

**Seats.** A vehicle with fewer seats than requested is recommended as blocked with `INSUFFICIENT_SEATS`. Reserving it directly returns `422 SEAT_CAPACITY_EXCEEDED`.

**Request limits.** `endAt` must be after `startAt` and at most 14 days later. `estimatedKm` is 1–5000, `seatsNeeded` is 1–60 (driver included) and `purpose` is 3–200 characters. Breaking these returns `400 VALIDATION_ERROR`.

**Who may read or cancel.** `GET /reservations` returns a staff member's own reservations and the rides they joined; a fleet manager receives every reservation. A staff member who opens another person's reservation with `GET /reservations/{id}` receives `403 FORBIDDEN`. Only a `CONFIRMED` reservation can be cancelled, and only by its owner or a fleet manager. Any other status (for example `ACTIVE`, after pickup) returns `409 RESERVATION_NOT_CANCELLABLE`.

**Ride sharing.** A request matches a trip with the same destination, departure within the tolerance window (default 30 minutes) and enough free seats. The trip must have `allowRideSharing` set. A departure 31 minutes away, a full vehicle, or sharing turned off by the driver is not returned by `GET /rides/matches`. Joining a ride that has a free seat returns `201` and `seatsAvailable` drops by one. A full ride returns `422 SEAT_CAPACITY_EXCEEDED`. Joining again returns `409 ALREADY_JOINED`. Leaving before the trip starts returns `204` and frees the seat. The passenger, the reservation owner or a fleet manager may do this. Removing a passenger from an `ACTIVE` ride returns `409 INVALID_RESERVATION_STATE`. Anyone else receives `403 FORBIDDEN`.

## Mock server for frontend development

Until the backend is implemented, the frontend uses a Prism mock server generated from `docs/openapi.yaml`.

```bash
npx @stoplight/prism-cli mock docs/openapi.yaml
```

The mock runs on `http://localhost:4010` (the second server in `openapi.yaml`) and returns the example responses defined in the contract.

Example:

```bash
curl http://localhost:4010/locations -H "Authorization: Bearer test"
```

`docs/api_usage.md` starts the same server with the version pinned (`npx @stoplight/prism-cli@5.12.0 mock docs/openapi.yaml -p 4010`). Prism already defaults to port 4010, so both commands serve the contract examples. A request body Prism cannot validate against the schema comes back as 422; the real backend uses `400 VALIDATION_ERROR` for field errors. The frontend should treat both as validation failures.
