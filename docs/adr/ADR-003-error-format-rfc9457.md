# ADR-003: Error responses follow RFC 9457 with a machine-readable code

- Status: Accepted
- Date: 2026-11-21
- Decider: Ali Eren Kurt (Lead Software Architect)
- Consulted: Ahmet Tarık Orhan (Backend & API), Mustafa Düşünceli (Frontend & UI), Abdullah Tecimen (QA)

## Context

FleetSync rejects many requests for business reasons, and the user must see why: a
vehicle is blocked for maintenance, a licence has expired, the period overlaps another
reservation. The frontend has to show a specific message and sometimes act on it (offer
`suggestedVehicleIds`). QA writes tests against the same errors. Several different rules
share one HTTP status (finding F6 in `docs/test_plans_and_coverage.md`), so the status
code alone is not enough. FastAPI's default error body (`{"detail": ...}`) has no stable
field to branch on.

## Decision

1. Every error response uses **RFC 9457 Problem Details** with media type
   `application/problem+json` and the `Problem` schema in `openapi.yaml`:
   `type`, `title`, `status`, `detail`, `instance`, plus two extensions:
   - `code` (required): a value of the `ErrorCode` enum. **Clients branch on `code`, never
     on `title` or `detail`.**
   - `errors` (400 only): field-level messages; `suggestedVehicleIds` for
     `VEHICLE_MAINTENANCE_DUE` and `RESERVATION_CONFLICT`.
2. HTTP status classes are used consistently:

   | Status | Meaning | Examples |
   |---|---|---|
   | 400 | Input is malformed or out of range | `VALIDATION_ERROR` |
   | 401 | No valid token | `UNAUTHORIZED`, `INVALID_CREDENTIALS` |
   | 403 | Role or ownership does not allow it | `FORBIDDEN` |
   | 404 | Resource does not exist | `NOT_FOUND` |
   | 409 | The current state of a resource prevents it | `RESERVATION_CONFLICT`, `VEHICLE_MAINTENANCE_DUE`, `INVALID_STATUS_TRANSITION` |
   | 422 | The request is valid but breaks a business rule about the caller or the data | `LICENSE_EXPIRED`, `SEAT_CAPACITY_EXCEEDED`, `ODOMETER_DECREASED` |

3. `type` is a stable URI per code: `https://fleetsync.local/problems/<code-in-kebab-case>`.
   `detail` is a human-readable sentence with the actual values (for example the two
   odometer readings).
4. Implementation: domain code raises `DomainError(code, detail, **extensions)`; one
   exception handler in `app/shared/problems.py` maps it to the response. FastAPI's
   `RequestValidationError` is mapped to `400 VALIDATION_ERROR` with `errors[]`, replacing
   FastAPI's default 422.
5. Adding a new `code` is a contract change: it goes into the `ErrorCode` enum in
   `openapi.yaml` first, through a reviewed PR.

## Alternatives considered

| Option | Why not |
|---|---|
| FastAPI default `{"detail": "..."}` | No stable field for the client; validation errors use 422, which clashes with our business-rule 422 |
| Custom error envelope (`{"error": {"code", "message"}}`) | Same information as RFC 9457 but non-standard; tools and reviewers already know RFC 9457 |
| Only HTTP status codes | Several rules share 409 and 422 (finding F6) |

## Consequences

- Positive: frontend messages, QA assertions and backend code all use the same `code`
  list from `openapi.yaml`.
- Positive: the jury can read `detail` directly in the demo.
- Negative: the Prism mock answers schema-invalid bodies with 422, not 400; the frontend
  treats both as validation errors (`docs/api_usage.md`).
- Follow-up: contract tests assert `Content-Type: application/problem+json` and a valid
  `code` for every documented error response (Sprint 3).

## Related

- RFC 9457, Problem Details for HTTP APIs
- `docs/openapi.yaml` `Problem`, `ErrorCode`
- `docs/carpool_reservation_api.md` (business rules and codes)
- Issue #242
