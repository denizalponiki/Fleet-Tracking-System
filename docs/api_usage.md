# FleetSync API contract

`docs/openapi.yaml` (OpenAPI 3.1) is the project's API contract; code is written against it. Changes go through a pull request approved by the Lead Architect and the owner of the affected module.

## Contents

| Module | Owner | Operations |
|---|---|---|
| auth | Ahmet Can Vurmaz (PO) | `POST /auth/login`, `GET /me`, `GET/POST /users` |
| drivers | Ahmet Can Vurmaz (PO) | `GET/PUT /drivers/{id}`, `GET/POST /drivers/{id}/licenses`, `POST /drivers/{id}/licenses/{licenseId}/verify`, `GET /drivers/{id}/eligibility` |
| locations | Ahmet Tarık Orhan (Backend) | `GET /locations` |
| vehicles | Ali Eren Kurt (Architect) | `GET/POST /vehicles`, `GET/PATCH /vehicles/{id}`, `POST /vehicles/{id}/status` |
| reservations | Ahmet Tarık Orhan (Backend) | `GET /vehicles/recommendations`, `GET/POST /reservations`, `GET /reservations/{id}`, `POST /reservations/{id}/cancel` |
| carpool | Ahmet Tarık Orhan (Backend) | `GET /rides/matches`, `POST /reservations/{id}/passengers`, `DELETE /reservations/{id}/passengers/{userId}` |
| handover | Mehmet Umut Oğuzcan (SM) | `GET /checklist-templates`, `POST /reservations/{id}/pickup`, `POST /reservations/{id}/return`, `POST /damage-reports`, `GET /vehicles/{id}/damage-reports` |
| maintenance | Ali Eren Kurt (Architect) | `GET /maintenance/rules`, `PUT /maintenance/rules/{id}`, `GET /vehicles/{id}/maintenance-status`, `GET /vehicles/{id}/maintenance-records`, `GET /maintenance/alerts`, `GET /maintenance/calendar`, `POST /maintenance/records` |
| fuel | Abdullah Tecimen (QA) | `POST /fuel-receipts`, `GET /vehicles/{id}/fuel-receipts`, `GET /vehicles/{id}/consumption`, `GET /fuel/anomalies`, `GET/POST /expenses` |
| reports | Deniz Alp Oniki (DevOps) | `GET /reports/summary`, `GET /reports/cost`, `GET /reports/carbon`, `GET /reports/utilization` |

39 paths and 46 operations in total.

## Shared conventions

- Base URL: `http://localhost:8080/api/v1`. Every request except `POST /auth/login` requires `Authorization: Bearer <JWT>`.
- Errors are returned as `application/problem+json` (RFC 9457). Clients branch on the `code` field:

  | HTTP | When | Example `code` |
  |---|---|---|
  | 400 | Field format error or missing required field | `VALIDATION_ERROR` |
  | 401 / 403 | Token missing / role not allowed | `UNAUTHORIZED`, `FORBIDDEN` |
  | 404 | Record not found | `NOT_FOUND` |
  | 409 | The resource's state does not allow the operation | `RESERVATION_CONFLICT`, `VEHICLE_MAINTENANCE_DUE`, `INVALID_RESERVATION_STATE` |
  | 422 | The request is well-formed but breaks a business rule | `LICENSE_EXPIRED`, `SEAT_CAPACITY_EXCEEDED`, `ODOMETER_DECREASED` |

- The examples use the same seed data as the jury demo: `06 FS 101` (oil change due in 100 km, blocked), `06 FS 102` (550 km left, recommended; enters maintenance on return at 60,020 km), `06 FS 103` (5 seats, not enough capacity).

## Validation (also runs in CI)

```bash
npx @redocly/cli@1.34.3 lint docs/openapi.yaml
```

Lint rules live in `redocly.yaml` at the repository root.

## Viewing the documentation

```bash
npx @redocly/cli@1.34.3 preview-docs docs/openapi.yaml
```

No-install option: paste the file into [editor.swagger.io](https://editor.swagger.io).

## Mock server (for the frontend)

The frontend is developed against this server until the backend is ready:

```bash
npx @stoplight/prism-cli@5.12.0 mock docs/openapi.yaml -p 4010
```

```bash
curl -H "Authorization: Bearer demo" "http://localhost:4010/vehicles/recommendations?startAt=2026-11-12T08:00:00%2B03:00&endAt=2026-11-13T19:00:00%2B03:00&seats=7&estimatedKm=400"
```

Use the `Prefer` header to request a specific error example:

```bash
curl -X POST -H "Authorization: Bearer demo" -H "Prefer: code=409, example=maintenanceDue" -H "Content-Type: application/json" -d "{\"vehicleId\":\"0b6f1c2a-0000-4000-8000-000000000101\",\"destinationId\":\"9c2b0000-0000-4000-8000-00000000c042\",\"purpose\":\"Konya\",\"startAt\":\"2026-11-12T08:00:00+03:00\",\"endAt\":\"2026-11-13T19:00:00+03:00\",\"estimatedKm\":400,\"seatsNeeded\":7}" http://localhost:4010/reservations
```

Note: Prism answers a request body that does not match the schema with 422, while the real backend answers field errors with 400. The frontend should show both as validation errors.

## Next steps

- At the end of Sprint 2 the contract is tagged `v1.0.0`. After that, breaking changes require a new version.
- The backend generates its controller interfaces from this file with `openapi-generator` (spring, `interfaceOnly=true`).
- The frontend generates its types with `openapi-typescript`.
